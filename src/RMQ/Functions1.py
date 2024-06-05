import sys, os
import pika
import json
from psycopg2.extras import DictCursor
import psycopg2
from datetime import datetime
import apiClient

class Functions:
    def __init__(self, request_ID):
        self.db_host = "175.45.214.45"
        self.db_port = "26257"
        self.db_database = "cdm_fix"
        self.db_user = "root"
        self.resource_db_schema = "rs_1717130387059"  # 스키마 이름 추가
        # self.resource_db_schema = "yuna"  # 스키마 이름 추가
        self.detail_db_schema = "detail"  # 스키마 이름 추가
        self.recovery_db_schema = "recovery"  # 스키마 이름 추가
        self.request_exchange = 'request_exchange'
        self.response_exchange = 'response_exchange'
        self.request_ID = request_ID
        self.api_client = apiClient.ApiClient()

    def connect_db(self):
        try:
            db_connection = psycopg2.connect(
                host=self.db_host,
                port=self.db_port,
                database=self.db_database,
                user=self.db_user,
            )
            return db_connection
        except Exception as e:
            print(f"DB 접속 오류입니다: {e}")

    def execute_query(self, query, params=None):
        conn = self.connect_db()
        cur = conn.cursor(cursor_factory=DictCursor)
        cur.execute("ROLLBACK;")
        cur.execute("BEGIN;")
        cur.execute(query, params)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    def execute_query_des(self, q):
        conn = self.connect_db()
        cur = conn.cursor(cursor_factory=DictCursor)
        cur.execute(q)
        rows = cur.fetchall()
        cols = [column[0] for column in cur.description]
        response = []
        for row in rows:
            response.append(dict(zip(cols, row)))
        cur.close()
        conn.close()
        return response

    def query_dbv(self, conn, q, v):
        # conn = self.connect_db()
        cur = conn.cursor(cursor_factory=DictCursor)
        cur.execute(q, v)
        conn.commit()
        cur.close()
        conn.close()

    def get_raw_data(self):
        raw_data = {
            "region": {},
            "zone": {},
            "vpc": {}
        }

        # Fetch and populate region data
        region_query = "SELECT regionid, regionname FROM region;"
        regions = self.execute_query(region_query)
        for region in regions:
            region_id = region['regionid']
            region_name = region['regionname']
            raw_data["region"][region_id] = region_name

        # Fetch and populate zone data
        zone_query = "SELECT zoneid, zonename FROM zone;"
        zones = self.execute_query(zone_query)
        for zone in zones:
            zone_id = zone['zoneid']
            zone_name = zone['zonename']
            raw_data["zone"][zone_id] = zone_name

        # Fetch and populate vpc data
        vpc_query = "SELECT vpcid, vpcname FROM vpc;"
        vpcs = self.execute_query(vpc_query)
        for vpc in vpcs:
            vpc_id = vpc['vpcid']
            vpc_name = vpc['vpcname']
            raw_data["vpc"][vpc_id] = vpc_name

        return raw_data

    def parse_query_result(self, rows):
        for row in rows:
            for key, value in row.items():
                if isinstance(value, datetime):
                    row[key] = value.isoformat()
        return json.loads(json.dumps([dict(row) for row in rows], indent=2))

    def create_response_message(self, request_code, message, reason, data):
        return {
            "response": {
                "id": self.request_ID,
                "code": request_code,
                "message": message,
                "reason": reason,
                "data": data
            }
        }
    def send_response(self, response_message, routing_key):
        response_message_str = json.dumps(response_message, indent=2)
        code = response_message['response']['code']
        print(f"response {code}\n{response_message_str}")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials('admin', 'admin')))
        channel = connection.channel()
        channel.exchange_declare(exchange=self.response_exchange, exchange_type='topic')
        channel.basic_publish(exchange=self.response_exchange, routing_key=routing_key,
                              body=json.dumps(response_message))
        # print(f"SEND '{response_message}' TO {self.response_exchange} WITH ROUTING_KEY {routing_key} FOR {self.request_ID}")
        connection.close()

    def handle_exception(self, code, exception):
        message = self.create_response_message(code, "fail", str(f"Exception Code: {code}, E: {exception}"), {})
        self.send_response(message, code)

    def receive_request(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials('admin', 'admin')))
        channel = connection.channel()
        channel.exchange_declare(exchange=self.request_exchange, exchange_type='topic')
        result = channel.queue_declare(queue='request_queue', exclusive=False)
        queue_name = result.method.queue
        channel.queue_bind(exchange=self.request_exchange, queue=queue_name, routing_key='common')

        def callback(ch, method, properties, body):
            # print(f"RECEIVED '{body}' FROM {self.request_exchange} WITH ROUTING_KEY 'common' FOR {self.request_ID}")
            body = body.decode('utf-8')
            body = json.loads(body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            result = self.process_request(body)
            if result:
                ch.stop_consuming()

        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)
        # print(f"Waiting for messages in {queue_name} with routing key 'common'")
        channel.start_consuming()

    def process_request(self, request_message):
        if 'request_code' not in request_message:
            print("Invalid request message: missing 'request_code'")
            print(request_message)
            return False

        if 'request_command' not in request_message:
            print("Invalid request message: missing 'request_command'")
            print(request_message)
            return False

        if 'request_data' not in request_message:
            print("Invalid request message: missing 'request_data'")
            print(request_message)
            return False

        code = request_message['request_code']
        command = request_message['request_command']
        data = request_message['request_data']

        if code == 'clusterinfo':
            self.Clusterinfo(command)
        elif code == 'instanceinfo':
            if command == 'get_all':
                self.Instanceinfo(command, data)
            elif command == 'get':
                if 'uuid' in data:
                    uuid = data['uuid']
                    self.Instanceinfo(command, uuid)
                else:
                    self.Instanceinfo(command, None)
        elif code == 'volume':
            if command == 'get_all':
                self.Volume(command, data)
            elif command == 'get':
                if 'instance' in data and 'uuid' in data['instance']:
                    uuid = data['instance']['uuid']
                    self.Volume(command, uuid)
                else:
                    self.Volume(command, None)
            elif command == 'create':
                pass
            elif command == 'create_sanpshot_volume':
                pass
            elif command == 'delete':
                pass
            elif command == 'attach':
                pass
            elif command == 'detach':
                pass
        # 우동
        # create
        # create_sanpshot_volume
        # delete
        # attach
        # detach

        elif code == 'snapshot':
            if command == 'get_all':
                self.VolumeSnapshot(command, data)
            elif command == 'get':
                if 'instance' in data and 'uuid' in data['instance']:
                    uuid = data['instance']['uuid']
                    self.VolumeSnapshot(command, uuid)
                else:
                    self.VolumeSnapshot(command, None)
        #lhb add
        elif code == 'resourceinfo':
            self.ResourceInfo(command, data)
        elif code == 'recoveryinfo':
            self.RecoveryInfo(command, data)
        
        return True

    def Clusterinfo(self, command):
        if command == 'get':
            try:
                query = f'''
                    SELECT vpc.*, region.regionname, region.regioncode,
                           zone.zonename, zone.zonecode, zone.zonedescription
                    FROM {self.resource_db_schema}.vpc
                    LEFT JOIN {self.resource_db_schema}.region ON vpc.regionid = region.id
                    LEFT JOIN {self.resource_db_schema}.zone ON vpc.regionid = zone.regionid;
                '''
                rows = self.execute_query(query)
                if not rows:
                    message = self.create_response_message("clusterinfo", "fail", "data not found", {})
                    self.send_response(message, "clusterinfo")
                    return
                result_json = self.parse_query_result(rows)
                row = result_json[0]
                m = {
                    "region": row['regionname'],
                    "zone": row['zonename'],
                    "uuid": row['vpcno'],
                    "name": row['vpcname'],
                    "status": row['vpcstatus'],
                    "raw": {
                        "vpc": {
                            "id": row['id'],
                            "regionid": row['regionid'],
                            "vpcno": row['vpcno'],
                            "vpcname": row['vpcname'],
                            "ipv4cidrblock": row['ipv4cidrblock'],
                            "vpcstatus": row['vpcstatus'],
                            "createdate": row['createdate']
                        },
                        "region": {
                            "regionname": row['regionname'],
                            "regioncode": row['regioncode']
                        },
                        "zone": {
                            "zonename": row['zonename'],
                            "zonecode": row['zonecode'],
                            "zonedescription": row['zonedescription']
                        }
                    }
                }

                message = self.create_response_message("clusterinfo", "success", "", {"cluster": m})
                self.send_response(message, "clusterinfo")

            except Exception as e:
                self.handle_exception("clusterinfo", e)
        elif command == 'sync':
            api_client = self.api_client
            res = api_client.sync_cluster()
            m = self.create_response_message("clusterinfo", "success", "", {"raw": res})
            self.send_response(m, "clusterinfo")
            print()


    def Instanceinfo(self, command, uuid):
        if command == 'get_all':
            try:
                query = f'SELECT * FROM {self.resource_db_schema}.serverinstance;'
                rows = self.execute_query(query)
                if not rows:
                    message = self.create_response_message("instanceinfo", "fail", "data not found", {})
                    self.send_response(message, "instanceinfo")
                    return
                result_json = self.parse_query_result(rows)
                final_result = []
                for i in range(len(result_json)):
                    m = {
                        "uuid": result_json[i]['serverinstanceno'],
                        "name": result_json[i]['servername'],
                        "status": result_json[i]['serverinstancestatusname'],
                        # "ip": result_json[i]['publicip'],
                        "raw": {"serverinstance": result_json[i]}
                    }
                    final_result.append(m)

                message = self.create_response_message("instanceinfo", "success", "", {"instance": final_result})
                self.send_response(message, "instanceinfo")

            except Exception as e:
                self.handle_exception("instanceinfo", e)

        elif command == 'get':
            try:
                m = []
                if not uuid:  # uuid가 빈 리스트인 경우
                    message = self.create_response_message("instanceinfo", "fail", "data not found", {})
                    self.send_response(message, "instanceinfo")
                    return
                for instance in uuid:
                    listkey = instance['uuid']
                    query = f'SELECT * FROM {self.resource_db_schema}.serverinstance WHERE serverinstanceno=%s;'
                    params = (listkey,)
                    rows = self.execute_query(query, params)
                    if not rows:
                        continue
                    result_json = self.parse_query_result(rows)
                    mm = {
                        "uuid": result_json[0]['serverinstanceno'],
                        "name": result_json[0]['servername'],
                        "status": result_json[0]['serverinstancestatusname'],
                        "ip": result_json[0]['publicip'],
                        "raw": {"serverinstance": result_json[0]}
                    }
                    m.append(mm)
                if not m:
                    message = self.create_response_message("instanceinfo", "fail", "data not found", {})
                    self.send_response(message, "instanceinfo")
                    return
                message = self.create_response_message("instanceinfo", "success", "", {"instance": m})
                self.send_response(message, "instanceinfo")
            except Exception as e:
                self.handle_exception("instanceinfo", e)

    def Volume(self, command, uuid):
        if command == 'get_all':
            try:
                query = f'SELECT * FROM {self.resource_db_schema}.blockstorageinstance;'
                rows = self.execute_query(query)
                if not rows:
                    message = self.create_response_message("volume", "fail", "data not found", {})
                    self.send_response(message, "volume")
                    return
                result_json = self.parse_query_result(rows)

                final_result = []
                for item in result_json:
                    volume = {
                        "instance": {
                            "uuid": item['serverinstanceno']
                        },
                        "volume": [
                            {
                                "uuid": item['blockstorageinstanceno'],
                                "name": item['blockstoragename'],
                                "type": item['blockstoragediskdetailtype'],
                                "size": item['blockstoragesize'],
                                "status": item['blockstorageinstancestatusname'],
                                "raw": {
                                    "blockstorageinstance": {"blockstorageinstanceno": item['blockstorageinstanceno']}}
                            }
                        ]
                    }
                    final_result.append(volume)

                message = self.create_response_message("volume", "success", "", {"instance_volume": final_result})
                self.send_response(message, "volume")

            except Exception as e:
                self.handle_exception("volume", e)

        elif command == 'get':
            try:
                instances = uuid
                instance_uuids = [instance['uuid'] for instance in instances]
                placeholders = ', '.join(['%s'] * len(instance_uuids))
                query = f'SELECT * FROM {self.resource_db_schema}.blockstorageinstance WHERE serverinstanceno IN ({placeholders});'
                rows = self.execute_query(query, instance_uuids)
                if not rows:
                    message = self.create_response_message("volume", "fail", "data not found", {})
                    self.send_response(message, "volume")
                    return
                result_json = self.parse_query_result(rows)

                final_result = []
                for item in result_json:
                    volume = {
                        "instance": {
                            "uuid": item['serverinstanceno']
                        },
                        "volume": [
                            {
                                "uuid": item['blockstorageinstanceno'],
                                "name": item['blockstoragename'],
                                "type": item['blockstoragediskdetailtype'],
                                "size": item['blockstoragesize'],
                                "status": item['blockstorageinstancestatusname'],
                                "raw": {
                                    "blockstorageinstance": {"blockstorageinstanceno": item['blockstorageinstanceno']}}
                            }
                        ]
                    }
                    final_result.append(volume)

                message = self.create_response_message("volume", "success", "", {"instance_volume": final_result})
                self.send_response(message, "volume")

            except Exception as e:
                self.handle_exception("volume", e)

    def VolumeSnapshot(self, command, data):
        if command == 'get_all':
            try:
                query = f'SELECT * FROM {self.resource_db_schema}.blockstoragesnapshotinstance;'
                rows = self.execute_query(query)
                if not rows:
                    message = self.create_response_message("snapshot", "fail", "data not found", {})
                    self.send_response(message, "snapshot")
                    return
                result_json = self.parse_query_result(rows)

                final_result = []
                for item in result_json:
                    snapshot = {
                        "instance": {
                            "uuid": item['serverinstanceno']
                        },
                        "volume": [
                            {
                                "uuid": item['blockstorageinstanceid'],
                                "snapshot": [
                                    {
                                        "uuid": item['blockstoragesnapshotinstanceno'],
                                        "name": item['blockstoragesnapshotname'],
                                        "size": item['blockstoragesnapshotvolumesize'],
                                        "status": item['blockstoragesnapshotinstancestatusname'],
                                        "type": item['snapshottype'],
                                        "date": item['createdate'],
                                        "raw": {"blockstoragesnapshotinstance": {
                                            "blockstoragesnapshotinstanceno": item['blockstoragesnapshotinstanceno']}}
                                    }
                                ]
                            }
                        ]
                    }
                    final_result.append(snapshot)

                message = self.create_response_message("snapshot", "success", "", {"instance_volume": final_result})
                self.send_response(message, "snapshot")

            except Exception as e:
                self.handle_exception("snapshot", e)

        elif command == 'get':
            try:
                instance_volumes = data.get('instance_volume', [])
                final_result = []
                for instance_volume in instance_volumes:
                    instance_uuid = instance_volume['instance']['uuid']
                    volume_uuids = [volume['uuid'] for volume in instance_volume['volume']]
                    placeholders = ', '.join(['%s'] * len(volume_uuids))
                    query = f'SELECT * FROM {self.resource_db_schema}.blockstoragesnapshotinstance WHERE serverinstanceno = %s AND blockstorageinstanceid IN ({placeholders});'
                    params = [instance_uuid] + volume_uuids
                    rows = self.execute_query(query, params)
                    if not rows:
                        continue
                    result_json = self.parse_query_result(rows)

                    snapshot_result = []
                    for item in result_json:
                        snapshot = {
                            "instance": {
                                "uuid": item['serverinstanceno']
                            },
                            "volume": [
                                {
                                    "uuid": item['blockstorageinstanceid'],
                                    "snapshot": [
                                        {
                                            "uuid": item['blockstoragesnapshotinstanceno'],
                                            "name": item['blockstoragesnapshotname'],
                                            "size": item['blockstoragesnapshotvolumesize'],
                                            "status": item['blockstoragesnapshotinstancestatusname'],
                                            "type": item['snapshottype'],
                                            "date": item['createdate'],
                                            "raw": {"blockstoragesnapshotinstance": {
                                                "blockstoragesnapshotinstanceno": item[
                                                    'blockstoragesnapshotinstanceno']}}
                                        }
                                    ]
                                }
                            ]
                        }
                        snapshot_result.append(snapshot)

                    final_result.extend(snapshot_result)

                if not final_result:
                    message = self.create_response_message("snapshot", "fail", "data not found", {})
                    self.send_response(message, "snapshot")
                    return

                message = self.create_response_message("snapshot", "success", "", {"instance_volume": final_result})
                self.send_response(message, "snapshot")

            except Exception as e:
                self.handle_exception("snapshot", e)

    # 2024.05.22 lhb add
    def convert_to_json(self, row):
        json_data = {}
        for key, value in row.items():
            if isinstance(value, datetime):
                json_data[key] = value.isoformat()
            else:
                json_data[key] = value
        return json_data

    def update_column_by_id(self, schema_name, table_name, column_name, uuid, new_value):
        """
        Update the column value in the given schema, table, and column.

        Parameters:
        - db_config (dict): Database configuration with keys 'dbname', 'user', 'password', 'host', and 'port'.
        - schema_name (str): The name of the schema.
        - table_name (str): The name of the table.
        - column_name (str): The name of the column to update.
        - old_value (str): The current value of the column.
        - new_value (str): The new value of the column.

        Returns:
        - None
        """

        # Establish connection to the database
        conn = self.connect_db()
        # Create a cursor object
        cursor = conn.cursor()

        # Define the SQL query
        update_query = f"""
        UPDATE {schema_name}.{table_name}
        SET {column_name} = %s
        WHERE id = %s;
        """
        print(update_query)
        try:
            # Execute the SQL query
            cursor.execute(update_query, (new_value, uuid))
            # Commit the transaction
            conn.commit()
            return "Success"

        except Exception as e:
            # If there is any error, rollback the transaction
            conn.rollback()
            return f"Fail with Exception: {e}"

        finally:
            # Close the cursor and connection
            cursor.close()
            conn.close()

    def ResourceInfo(self, command, data):
        req_code = "resourceinfo"
        if command == 'get':
            try:
                api_client = self.api_client
                res = api_client.source_to_target()
                m = self.create_response_message(req_code, "success", "", {"raw": res})
                self.send_response(m, req_code)
            except Exception as e:
                self.handle_exception(req_code, e)
        elif command == 'set':
            try:
                # detail_db_schema 스키마에 저장할 데이터 추출
                # resource_data = data.get('instance', [])
                resource_data = data.get('raw')
                api_client = self.api_client
                res = api_client.set_resource_info(resource_data)
                message = self.create_response_message(req_code, "success", "", {"raw": res})
                self.send_response(message, req_code)
            except Exception as e:
                self.handle_exception(req_code, e)
        elif command == 'update':
            try:
                # detail_db_schema 스키마에 저장할 데이터 추출
                # resource_data = data.get('instance', [])
                # def update_column_by_id(self, schema_name, table_name, column_name, uuid, new_value):

                queries = data.get('instance')

                # 타겟 DB에 접속해서 가장 최신 스키마에 대해 raw SQL 실행


                schemas = self.execute_query_des("show schemas;")
                last_schema = [schema['schema_name'] for schema in schemas if schema['schema_name'].startswith('ds_')]
                print(">>>>", last_schema)
                last_schema = max(last_schema)
                print(">>>>", last_schema)

                res = ""
                for query in queries:
                    res = self.update_column_by_id(last_schema, query['table_name'], query['column_name'], query['uuid'], query['new_value'])

                message = self.create_response_message(req_code, "success", "", {"raw": res})
                self.send_response(message, req_code)

            except Exception as e:
                self.handle_exception(req_code, e)


    def RecoveryInfo(self, command, data):
        if command == 'get' or command == 'status':
            cmd = command
            try:
                query = f'''
                    SELECT si.*, p.productname, p.producttype, r.regionname, z.zonename, vpc.vpcname, s.subnetname, s.subnet
                    FROM {self.resource_db_schema}.serverinstance si
                    JOIN {self.resource_db_schema}.product p ON si.serverproductcodeid = p.id
                    JOIN {self.resource_db_schema}.region r ON si.regionid = r.id  
                    JOIN {self.resource_db_schema}.zone z ON si.zoneid = z.id
                    JOIN {self.resource_db_schema}.vpc vpc ON si.vpcid = vpc.id
                    JOIN {self.resource_db_schema}.subnet s ON si.subnetid = s.id;
                '''
                server_instance_rows = self.execute_query(query)
                if not server_instance_rows:
                    message = self.create_response_message(cmd, "fail", "data not found", {})
                    self.send_response(message, cmd)
                    return

                # 서버인스턴스와 연관된 테이블 조회
                server_instance_ids = [row['id'] for row in server_instance_rows]
                placeholders = ', '.join(['%s'] * len(server_instance_ids))

                # 액티비티로그 테이블 조회
                query_activitylog = f'''
                    SELECT *
                    FROM {self.resource_db_schema}.activitylog
                    WHERE serverinstanceid IN ({placeholders});
                '''
                activitylog_rows = self.execute_query(query_activitylog, server_instance_ids)

                # 네트워크인터페이스 테이블 조회
                query_networkinterface = f'''
                    SELECT ni.*, s.subnetname, s.subnet
                    FROM {self.resource_db_schema}.networkinterface ni
                    JOIN {self.resource_db_schema}.subnet s ON ni.subnetid = s.id
                    WHERE ni.instanceno IN (SELECT serverinstanceno FROM {self.resource_db_schema}.serverinstance WHERE id IN ({placeholders}));
                '''
                networkinterface_rows = self.execute_query(query_networkinterface, server_instance_ids)

                # 퍼블릭IP 테이블 조회
                query_publicip = f'''
                    SELECT *
                    FROM {self.resource_db_schema}.publicipinstance
                    WHERE serverinstanceno IN (SELECT serverinstanceno FROM {self.resource_db_schema}.serverinstance WHERE id IN ({placeholders}));
                '''
                publicip_rows = self.execute_query(query_publicip, server_instance_ids)

                # 결과 데이터 생성
                recovery_data = []
                for row in server_instance_rows:
                    server_instance_data = {"serverInstance": dict(row), "activityLogs": []}

                    # 액티비티로그 추가
                    for log_row in activitylog_rows:
                        if log_row['serverinstanceid'] == row['id']:
                            server_instance_data["activityLogs"].append({"activityLog": dict(log_row)})

                    # 네트워크인터페이스 추가
                    server_instance_data["networkInterfaces"] = []
                    for ni_row in networkinterface_rows:
                        if ni_row['instanceno'] == row['serverinstanceno']:
                            server_instance_data["networkInterfaces"].append({"networkInterface": dict(ni_row)})

                    # 퍼블릭IP 추가
                    server_instance_data["publicIps"] = []
                    for publicip_row in publicip_rows:
                        if publicip_row['serverinstanceno'] == row['serverinstanceno']:
                            server_instance_data["publicIps"].append({"publicIp": dict(publicip_row)})

                    recovery_data.append(server_instance_data)

                message = self.create_response_message(cmd, "success", "", {"data": recovery_data})
                self.send_response(message, cmd)

            except Exception as e:
                self.handle_exception(cmd, e)
        elif command == 'update':
            try:
                # recoveryinfo update 명령어 처리 로직 구현
                # data 파라미터를 사용하여 필요한 데이터 추출 및 가공
                # DB 쿼리 실행 및 결과 처리
                # 응답 메시지 생성 및 전송
                pass
            except Exception as e:
                self.handle_exception("recoveryinfo", e)