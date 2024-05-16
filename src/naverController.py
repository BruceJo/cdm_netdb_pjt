import pika
import json
from psycopg2.extras import DictCursor
import psycopg2
from datetime import datetime
from datetime import date


class Functions:
    def __init__(self):
        self.db_host = "175.45.214.45"
        self.db_port = "26257"
        self.db_database = "cdm_fix"
        self.db_user = "root"
        self.request_queue = 'request_queue'
        self.response_queue = 'response_queue'

    def connect_cockroachdb(self):
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

    def receive_request(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials('admin', 'admin')))
        channel = connection.channel()
        channel.queue_declare(queue=self.request_queue)
        method_frame, header_frame, body = channel.basic_get(queue=self.request_queue, auto_ack=True)
        if method_frame:
            body = body.decode('utf-8')
            request_message = json.loads(body)
            request_id = request_message['request']['id']
            print(f"RECEVIED '{body}' FROM {self.request_queue} FOR {request_id}")
        else:
            print(f" [!] No message in {self.request_queue}")
            connection.close()
            return

        code = request_message['request']['code']
        command = request_message['request']['parameter']['command']
        ukey = request_message['request']['parameter']['data'].get('ukey', None)
        data = request_message['request']['parameter']['data']

        if code == 'clusterinfo':
            if command == 'get':
                self.get_clusterinfo(request_id)
            elif command == 'sync':
                self.sync_clusterinfo(request_id)
        elif code == 'instanceinfo':
            if command == 'get':
                self.get_instanceinfo(request_id)
        elif code == 'volumeinfo':
            if command == 'get':
                self.get_volumeinfo(request_id)
            else:
                self.process_volumeinfo(request_id, command, data)
        elif code == 'snapshotinfo':
            if command == 'get':
                self.get_snapshotinfo(request_id)
            else:
                self.process_snapshotinfo(request_id, command, data)
        elif code == 'recoveryjob':
            self.process_recoveryjob(request_id, command, data)
        elif code == 'resourceinfo':
            if command == 'get':
                self.get_resourceinfo(request_id)
            elif command == 'set':
                self.set_resourceinfo(request_id)
        elif code == 'recoveryinfo':
            if command == 'get':
                self.get_recoveryinfo(request_id)
            elif command == 'status':
                self.status_recoveryinfo(request_id)
            elif command == 'update':
                self.update_recoveryinfo(request_id)

        connection.close()

    def send_response(self, request_id, response_message):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials('admin', 'admin')))
        channel = connection.channel()
        channel.queue_declare(queue=self.response_queue)
        channel.basic_publish(exchange='', routing_key=self.response_queue, body=json.dumps(response_message))
        print(f"SEND '{response_message}' TO {self.response_queue} FOR {request_id}")
        connection.close()

    def get_clusterinfo(self, request_id):
        try:
            conn = self.connect_cockroachdb()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            # 모든 테이블 조회
            tables = [
                'accesscontrolgroup', 'adjustmenttype', 'inautoscalinggroupserverinstance', 'initscript',
                'loadbalancerruleaction', 'loadbalancerrulecondition', 'loginkey', 'memberserverimageinstance',
                'placementgroup', 'product', 'protocoltype', 'publicipinstance', 'region', 'accesscontrolgrouprule',
                'launchconfiguration', 'vpc', 'vpcpeeringinstance', 'zone', 'blockstorageinstance',
                'blockstoragesnapshotinstance', 'loadbalancerinstance', 'loadbalancerlistener', 'loadbalancerrule',
                'memberserverimage', 'networkacl', 'networkacldenyallowgroup', 'networkaclrule', 'routetable',
                'subnet', 'autoscalinggroup', 'loadbalancersubnet', 'natgatewayinstance', 'networkinterface',
                'route', 'scalingpolicy', 'scheduledupdategroupaction', 'serverinstance', 'activitylog',
                'targetgroup', 'recoveryplan', 'recoveryresults'
            ]

            result = {}
            for table in tables:
                cur.execute(f"SELECT * FROM test0409t.{table}")
                rows = cur.fetchall()

                # datetime 객체를 문자열로 변환
                for row in rows:
                    for key, value in row.items():
                        if isinstance(value, datetime):
                            row[key] = value.isoformat()
                        elif isinstance(value, date):
                            row[key] = value.isoformat()
                result[table] = rows

            result = [result]
            message = {
                "response": {
                    "id": request_id,
                    "code": "clusterinfo",
                    "message": "success",
                    "reason": "",
                    "data": result
                }
            }
            self.send_response(request_id, message)
            cur.close()
            conn.close()

        except Exception as e:
            message = {
                "response": {
                    "id": request_id,
                    "code": "clusterinfo",
                    "message": "fail",
                    "reason": f"{e}",
                    "data": {}
                }
            }
            self.send_response(request_id, message)

    def sync_clusterinfo(self, request_id):
        pass

    def get_instanceinfo(self, request_id):
        try:
            conn = self.connect_cockroachdb()
            cur = conn.cursor()

            cur.execute("SELECT * FROM test0409t.serverinstance")
            rows = cur.fetchall()

            message = {
                "response": {
                    "id": request_id,
                    "code": "instanceinfo",
                    "message": "success",
                    "reason": "",
                    "data": rows
                }
            }
            self.send_response(request_id, message)
            cur.close()
            conn.close()

        except Exception as e:
            message = {
                "response": {
                    "id": request_id,
                    "code": "instanceinfo",
                    "message": "fail",
                    "reason": f"{e}",
                    "data": {}
                }
            }
            self.send_response(request_id, message)

    def get_resourceinfo(self, request_id):
        pass

    def set_resourceinfo(self, request_id):
        pass

    def get_recoveryinfo(self, request_id):
        pass

    def status_recoveryinfo(self, request_id):
        pass

    def update_recoveryinfo(self, request_id):
        pass

    def process_recoveryjob(self, request_id, command, data):
        if command == 'run':
            pass
        elif command == 'pause':
            pass
        elif command == 'stop':
            pass
        elif command == 'rollback':
            pass

    def get_volumeinfo(self, request_id):
        try:
            conn = self.connect_cockroachdb()
            cur = conn.cursor()

            cur.execute("SELECT * FROM blockstorageinstance")
            rows = cur.fetchall()

            message = {
                "response": {
                    "id": request_id,
                    "code": "volumeinfo",
                    "message": "success",
                    "reason": "",
                    "data": rows
                }
            }
            self.send_response(request_id, message)
            cur.close()
            conn.close()

        except Exception as e:
            message = {
                "response": {
                    "id": request_id,
                    "code": "volumeinfo",
                    "message": "fail",
                    "reason": f"{e}",
                    "data": {}
                }
            }
            self.send_response(request_id, message)

    def process_volumeinfo(self, request_id, command, data):
        if command == 'create':
            pass
        elif command == 'delete':
            pass
        elif command == 'attach':
            pass
        elif command == 'detach':
            pass

    def get_snapshotinfo(self, request_id):
        try:
            conn = self.connect_cockroachdb()
            cur = conn.cursor()

            cur.execute("SELECT * FROM blockstoragesnapshotinstance")
            rows = cur.fetchall()

            message = {
                "response": {
                    "id": request_id,
                    "code": "snapshotinfo",
                    "message": "success",
                    "reason": "",
                    "data": rows
                }
            }
            self.send_response(request_id, message)
            cur.close()
            conn.close()

        except Exception as e:
            message = {
                "response": {
                    "id": request_id,
                    "code": "snapshotinfo",
                    "message": "fail",
                    "reason": f"{e}",
                    "data": {}
                }
            }
            self.send_response(request_id, message)

    def process_snapshotinfo(self, request_id, command, data):
        if command == 'create':
            pass
        elif command == 'delete':
            pass

    def process_data(self, request_id, code, table_name, join_keys, mapping_func, ukey=None):
        try:
            conn = self.connect_cockroachdb()
            cur = conn.cursor(cursor_factory=DictCursor)
            cur.execute("ROLLBACK;")
            cur.execute("BEGIN;")

            query = f'SELECT * FROM yuna.{table_name}'
            if ukey:
                query += f' WHERE {table_name}no=%s'
                print(f"code: {code} / command: get / query: ", query)
                cur.execute(query, (ukey,))
            else:
                print(f"code: {code} / command: get / query: ", query)
                cur.execute(query)

            rows = cur.fetchall()
            for row in rows:
                for key, value in row.items():
                    if isinstance(value, datetime):
                        row[key] = value.isoformat()

            result = json.dumps([dict(row) for row in rows], indent=2)
            result_json = json.loads(result)

            final_result = mapping_func(cur, result_json, join_keys, ukey)

            message = {
                "response": {
                    "id": request_id,
                    "code": code,
                    "message": "success",
                    "reason": "",
                    "data": final_result
                }
            }
            self.send_response(request_id, message)
            cur.close()
            conn.close()

        except Exception as e:
            message = {
                "response": {
                    "id": request_id,
                    "code": code,
                    "message": "fail",
                    "reason": f"{e}",
                    "data": {
                        code: ""
                    }
                }
            }
            self.send_response(request_id, message)

    def map_cluster_data(self, cur, result_json, join_keys, ukey):
        final_result = []
        for i in range(len(result_json)):
            for key in join_keys:
                cur.execute(f"SELECT regionname FROM yuna.region WHERE id=%s;", (result_json[i][key],))
                fetch_result = cur.fetchone()
                result_json[i][key.replace("id", "name")] = fetch_result[0] if fetch_result else ""

            m = {
                "region": result_json[i]['regionname'],
                "zone": "",
                "uuid": result_json[i]['vpcno'],
                "name": result_json[i]['vpcname'],
                "status": result_json[i]['vpcstatus'],
                "raw": result_json[i]
            }
            final_result.append(m)

        return {"cluster": final_result}

    def map_instance_data(self, cur, result_json, join_keys, ukey):
        final_result = []
        for i in range(len(result_json)):
            m = {
                "uuid": result_json[i]['serverinstanceno'],
                "name": result_json[i]['servername'],
                "status": result_json[i]['serverinstancestatusname'],
                "ip": result_json[i]['publicip'],
                "raw": result_json[i]
            }
            if ukey:
                final_result = m
            else:
                final_result.append(m)

        return {"instance": final_result}

    def map_instance_volume_data(self, cur, result_json, join_keys, ukey):
        final_result = {}
        for i in range(len(result_json)):
            uuid = result_json[i]['serverinstanceno']
            volume = {
                "uuid": result_json[i]['blockstorageinstanceno'],
                "name": result_json[i]['blockstoragename'],
                "size": result_json[i]['blockstoragesize'],
                "status": result_json[i]['blockstorageinstancestatusname'],
                "raw": {"blockstorageinstance": result_json[i]}
            }
            if uuid not in final_result:
                final_result[uuid] = {
                    "uuid": uuid,
                    "instance_volume": [volume]
                }
            else:
                final_result[uuid]['instance_volume'].append(volume)

        final_list = list(final_result.values())
        if ukey:
            final_list = [instance for instance in final_list if instance['uuid'] == ukey]

        return {"instance": final_list}

    def map_instance_volume_snapshot_data(self, cur, result_json, join_keys, ukey):
        final_result = {}
        for i in range(len(result_json)):
            uuid = result_json[i]['blockstorageinstanceid']
            volume = {
                "uuid": result_json[i]['blockstoragesnapshotinstanceno'],
                "name": result_json[i]['blockstoragesnapshotname'],
                "size": result_json[i]['blockstoragesnapshotvolumesize'],
                "status": result_json[i]['blockstoragesnapshotinstancestatusname'],
                "raw": {"blockstoragesnapshotinstance": result_json[i]}
            }
            if uuid not in final_result:
                final_result[uuid] = {
                    "uuid": uuid,
                    "instance_volume_snapshot": [volume]
                }
            else:
                final_result[uuid]['instance_volume_snapshot'].append(volume)

        final_list = list(final_result.values())
        return {"instance_volume": final_list}
