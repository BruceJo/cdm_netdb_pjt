import sys, os
import time

import pika
import json
from psycopg2.extras import DictCursor
import psycopg2
from datetime import datetime
import apiClient
import re
import pprint


class Functions:
    def __init__(self, request_ID):
        self.db_host = "175.45.214.45"
        self.db_port = "26257"
        self.db_database = "cdm_fix"
        self.db_user = "root"
        self.resource_db_schema = "rs_1717130387059"  # 스키마 이름 추가
        # self.resource_db_schema = "rs_1720136819613"
        # self.resource_db_schema = "yuna"  # 스키마 이름 추가
        self.detail_db_schema = "detail"  # 스키마 이름 추가
        self.recovery_db_schema = "recovery"  # 스키마 이름 추가
        self.request_exchange = 'request_exchange'
        self.response_exchange = 'response_exchange'
        self.request_ID = request_ID
        self.api_client = apiClient.ApiClient()
        self.set_lastest_schema_ds()
        self.set_lastest_schema_rs()

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

    def set_lastest_schema_rs(self):
        schema_list = [x['schema_name'] for x in self.query_db("show schemas;") if x['schema_name'][:3] == 'rs_']
        last_schema = max(schema_list)
        if self.resource_db_schema != last_schema:
            # print(f">>> schema name changed from {self.resource_db_schema} to {last_schema} <<<")
            self.resource_db_schema = last_schema
        return

    def set_lastest_schema_ds(self):
        schema_list = [x['schema_name'] for x in self.query_db("show schemas;") if x['schema_name'][:3] == 'ds_']
        last_schema = max(schema_list)
        if self.detail_db_schema != last_schema:
            # print(f">>> schema name changed from {self.resource_db_schema} to {last_schema} <<<")
            self.detail_db_schema = last_schema
        return

    def query_db(self, q):
        conn = self.connect_db()
        cur = conn.cursor()

        cur.execute(f"use {self.db_database};")
        cur.execute(q)
        rows = cur.fetchall()
        cols = [column[0] for column in cur.description]

        response = []
        for row in rows:
            response.append(dict(zip(cols, row)))

        cur.close()
        conn.close()

        return response

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
        if v:
            cur.execute(q, v)
        else:
            cur.execute(q)
        conn.commit()
        cur.close()
        conn.close()

    def query_dbv2(self, q, v):
        conn = self.connect_db()
        cur = conn.cursor(cursor_factory=DictCursor)
        if v:
            cur.execute(q, v)
        else:
            cur.execute(q)
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
        self.set_lastest_schema_rs()
        self.set_lastest_schema_ds()
        # print("req message")
        # print(request_message)
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

        print(f"code: {code}, command: {command}, data: {data}")

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
            elif command == 'reboot':
                for instance_info in data['instance']:
                    uuid = instance_info['uuid']
                    self.Instanceinfo(command, uuid)
        elif code == 'volumeinfo':
            if command == 'get_all':
                self.Volume(command, data)
            elif command == 'get':
                self.Volume(command, data)
            elif command == 'create' or 'delete' or 'detach':
                self.Volume(command, data)
            elif command == 'create_snapshot_volume':
                self.Volume(command, data)

        elif code == 'snapshotinfo':
            if command == 'get_all':
                self.VolumeSnapshot(command, data)
            elif command == 'get':
                if 'instance_volume' in data and 'uuid' in data['instance_volume']:
                    uuid = data['instance_volume']['uuid']
                    self.VolumeSnapshot(command, uuid)
                else:
                    self.VolumeSnapshot(command, None)
            elif command == 'delete':
                self.VolumeSnapshot(command, data)
            elif command == 'create':
                self.VolumeSnapshot(command, data)
        # lhb add
        elif code == 'resourceinfo':
            self.ResourceInfo(command, data)
        elif code == 'recoveryinfo':
            self.RecoveryInfo(command, data)
        elif code == 'recoveryjob':
            self.RecoveryJob(command, data)

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
        code = 'instanceinfo'
        if command == 'get_all':
            try:
                query = f'SELECT * FROM {self.resource_db_schema}.serverinstance;'
                rows = self.execute_query(query)
                if not rows:
                    message = self.create_response_message(code, "fail", "data not found", {})
                    self.send_response(message, code)
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

                message = self.create_response_message(code, "success", "", {"instance": final_result})
                self.send_response(message, code)

            except Exception as e:
                self.handle_exception(code, e)

        elif command == 'get':
            try:
                m = []
                if not uuid:  # uuid가 빈 리스트인 경우
                    message = self.create_response_message(code, "fail", "data not found", {})
                    self.send_response(message, code)
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
                    message = self.create_response_message(code, "fail", "data not found", {})
                    self.send_response(message, code)
                    return
                message = self.create_response_message(code, "success", "", {"instance": m})
                self.send_response(message, code)
            except Exception as e:
                self.handle_exception(code, e)

        elif command == 'reboot':
            try:
                api_client = self.api_client
                m = {
                    "request": {
                        "code": code,
                        "parameter": {
                            "command": command,
                            "data": {
                                "instance": [
                                    {
                                        "uuid": uuid
                                    }
                                ]
                            }
                        }
                    }
                }
                res = api_client.reboot_serverinstances(m)
                message = self.create_response_message(code, "success", "", {"raw": res})

                self.send_response(message, code)
            except Exception as e:
                self.handle_exception(code, e)

    def Volume(self, command, data):
        code = "volumeinfo"
        # uuid는 main 자원의 uuid, 실행되는 주체가 볼륨이라면 볼륨 uuid
        if command == 'get_all':
            try:
                query = f'SELECT * FROM {self.resource_db_schema}.blockstorageinstance;'
                rows = self.execute_query(query)
                if not rows:
                    message = self.create_response_message(code, "fail", "data not found", {})
                    self.send_response(message, code)
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

                message = self.create_response_message(code, "success", "", {"instance_volume": final_result})
                self.send_response(message, code)

            except Exception as e:
                self.handle_exception(code, e)

        # elif command == 'get':
        #     try:
        #         print(">>>>", data)
        #         uuid = data['instance'][0]['uuid']
        #         print(">>>>",uuid)
        #         instances = data['instance']
        #         instance_uuids = [instance['uuid'] for instance in data['instance']]
        #         placeholders = ', '.join(['%s'] * len(instance_uuids))
        #         # print(self.resource_db_schema)
        #         self.resource_db_schema = "rs_1725883178685"    # 테스트용
        #         query = f'SELECT * FROM {self.resource_db_schema}.blockstorageinstance WHERE serverinstanceno IN ({placeholders});'
        #         print(query)
        #         rows = self.execute_query(query, instance_uuids)
        #         if not rows:
        #             message = self.create_response_message(code, "fail", "data not found", {})
        #             self.send_response(message, code)
        #             return
        #         result_json = self.parse_query_result(rows)

        #         final_result = []
        #         for item in result_json:
        #             volume = {
        #                 "instance": {
        #                     "uuid": item['serverinstanceno']
        #                 },
        #                 "volume": [
        #                     {
        #                         "uuid": item['blockstorageinstanceno'],
        #                         "name": item['blockstoragename'],
        #                         "type": item['blockstoragediskdetailtype'],
        #                         "size": item['blockstoragesize'],
        #                         "status": item['blockstorageinstancestatusname'],
        #                         "raw": {
        #                             "blockstorageinstance": {"blockstorageinstanceno": item['blockstorageinstanceno']}}
        #                     }
        #                 ]
        #             }
        #             final_result.append(volume)

        #         message = self.create_response_message(code, "success", "", {"instance_volume": final_result})
        #         self.send_response(message, code)

        #     except Exception as e:
        #         self.handle_exception(code, e)
        elif command == 'get': # 0920 종우수정
            try:
                print(">>>>", data)
                instances = data['instance']
                instance_uuids = [instance['uuid'] for instance in instances]
                placeholders = ', '.join(['%s'] * len(instance_uuids))
                self.resource_db_schema = "rs_1725883178685"  # 테스트용
                query = f'SELECT * FROM {self.resource_db_schema}.blockstorageinstance WHERE serverinstanceno IN ({placeholders});'
                print(query)
                rows = self.execute_query(query, instance_uuids)
                if not rows:
                    message = self.create_response_message(code, "fail", "data not found", {})
                    self.send_response(message, code)
                    return
                result_json = self.parse_query_result(rows)

                # 딕셔너리로 instance uuid별로 볼륨 합치기
                instance_volume_dict = {}
                for item in result_json:
                    instance_uuid = item['serverinstanceno']
                    volume = {
                        "uuid": item['blockstorageinstanceno'],
                        "name": item['blockstoragename'],
                        "type": item['blockstoragediskdetailtype'],
                        "size": item['blockstoragesize'],
                        "status": item['blockstorageinstancestatusname'],
                        "raw": {
                            "blockstorageinstance": {"blockstorageinstanceno": item['blockstorageinstanceno']}
                        }
                    }

                    if instance_uuid not in instance_volume_dict:
                        # 새로운 instance uuid를 발견하면 새로 추가
                        instance_volume_dict[instance_uuid] = {
                            "uuid": instance_uuid,
                            "volume": []
                        }

                    # 해당 instance uuid에 볼륨 추가
                    instance_volume_dict[instance_uuid]["volume"].append(volume)

                # 결과를 리스트로 변환
                final_result = list(instance_volume_dict.values())

                message = self.create_response_message(code, "success", "", {"instance": final_result})
                self.send_response(message, code)

            except Exception as e:
                self.handle_exception(code, e)


        # elif command in ['create', 'delete', 'detach', 'attach', 'create_snapshot_volume']:
        #     try:
        #         api_client = self.api_client
        #         m = {
        #             "request": {
        #                 "code": code,
        #                 "parameter": {
        #                     "command": command,
        #                     "data": data
        #                 }
        #             }
        #         }
        #         res = api_client.modify_volume(m)
        #         print(">>>>",res)
        #         res_dict = json.loads(res)

        #         response_key = next((key for key in res_dict.keys() if key.endswith('Response')), None)
        #         if response_key:
        #             storage_list = res_dict[response_key]['blockStorageInstanceList']
        #         elif 'blockStorageSnapshotInstanceList' in res_dict[response_key]:
        #             storage_list = res_dict[response_key]['blockStorageSnapshotInstanceList']
        #         else:
        #             raise ValueError("Unexpected API response format")

        #         instance_volumes = []
        #         for refine_dict in storage_list:
        #             # 추출된 정보를 딕셔너리에 저장
        #             structured_data = {
        #                 "serverinstanceno": refine_dict.get('serverInstanceNo'),
        #                 "blockstorageinstanceno": refine_dict.get('blockStorageInstanceNo') or refine_dict.get(
        #                     'blockStorageSnapshotInstanceNo'),
        #                 "blockstoragesnapshotinstanceno": refine_dict.get('blockStorageSnapshotInstanceNo'),
        #                 "originalblockstorageinstanceno": refine_dict.get('originalBlockStorageInstanceNo')
        #             }

        #             # 볼륨 정보 구성
        #             volume_info = {
        #                 "uuid": structured_data["blockstorageinstanceno"],
        #                 "name": refine_dict.get('blockStorageName') or refine_dict.get('blockStorageSnapshotName'),
        #                 "type": refine_dict.get('blockStorageDiskDetailType', {}).get('codeName'),
        #                 "size": refine_dict.get('blockStorageSize') or refine_dict.get(
        #                     'blockStorageSnapshotVolumeSize'),
        #                 "status": refine_dict.get('blockStorageInstanceStatusName') or refine_dict.get(
        #                     'blockStorageSnapshotInstanceStatusName'),
        #                 "snapshot": None if command != 'create_snapshot_volume' else structured_data[
        #                     "blockstoragesnapshotinstanceno"],
        #                 "raw": refine_dict
        #             }

        #             instance_volumes.append({
        #                 "instance": {
        #                     "uuid": structured_data["serverinstanceno"]
        #                 },
        #                 "volume": volume_info
        #             })

        #         message = self.create_response_message(code, "success", "", {
        #             "instance_volume": instance_volumes
        #         })
        #         self.send_response(message, code)

        #     except Exception as e:
        #         self.handle_exception(code, e)

        # 0923 종우수정
        elif command in ['create', 'delete', 'detach', 'attach', 'create_snapshot_volume']:
            try:
                api_client = self.api_client
                m = {
                    "request": {
                        "code": code,
                        "parameter": {
                            "command": command,
                            "data": data
                        }
                    }
                }
                res = api_client.modify_volume(m)
                print(">>>>", res)
                res_dict = json.loads(res)

                response_key = next((key for key in res_dict.keys() if key.endswith('Response')), None)
                if response_key:
                    storage_list = res_dict[response_key]['blockStorageInstanceList']
                elif 'blockStorageSnapshotInstanceList' in res_dict[response_key]:
                    storage_list = res_dict[response_key]['blockStorageSnapshotInstanceList']
                else:
                    raise ValueError("Unexpected API response format")

                instance_volumes = []
                for refine_dict in storage_list:
                    # 추출된 정보를 딕셔너리에 저장
                    structured_data = {
                        "serverinstanceno": refine_dict.get('serverInstanceNo'),
                        "blockstorageinstanceno": refine_dict.get('blockStorageInstanceNo') or refine_dict.get(
                            'blockStorageSnapshotInstanceNo'),
                        "blockstoragesnapshotinstanceno": refine_dict.get('blockStorageSnapshotInstanceNo'),
                        "originalblockstorageinstanceno": refine_dict.get('originalBlockStorageInstanceNo')
                    }

                    # 볼륨 정보 구성 (리스트로 변경)
                    volume_info = [{
                        "uuid": structured_data["blockstorageinstanceno"],
                        "name": refine_dict.get('blockStorageName') or refine_dict.get('blockStorageSnapshotName'),
                        "type": refine_dict.get('blockStorageDiskDetailType', {}).get('codeName'),
                        "size": refine_dict.get('blockStorageSize') or refine_dict.get('blockStorageSnapshotVolumeSize'),
                        "status": refine_dict.get('blockStorageInstanceStatusName') or refine_dict.get('blockStorageSnapshotInstanceStatusName'),
                        "snapshot": [] if command != 'create_snapshot_volume' else [structured_data["blockstoragesnapshotinstanceno"]],
                        "raw": refine_dict
                    }]

                    # 기존 instance를 찾고 볼륨을 추가하는 부분
                    existing_instance = next((item for item in instance_volumes if item["instance"]["uuid"] == structured_data["serverinstanceno"]), None)
                    if existing_instance:
                        existing_instance["volume"].extend(volume_info)
                    else:
                        # 새로운 instance를 추가
                        instance_volumes.append({
                            "instance": {
                                "uuid": structured_data["serverinstanceno"]
                            },
                            "volume": volume_info
                        })

                message = self.create_response_message(code, "success", "", {
                    "instance_volume": instance_volumes
                })
                self.send_response(message, code)

            except Exception as e:
                self.handle_exception(code, e)


    def VolumeSnapshot(self, command, data):
        print(f"volume snapshot > {command} {data}")
        code = 'snapshotinfo'
        if command == 'get_all':
            try:
                query = f'SELECT * FROM {self.resource_db_schema}.blockstoragesnapshotinstance;'
                rows = self.execute_query(query)
                if not rows:
                    message = self.create_response_message(code, "fail", "data not found", {})
                    self.send_response(message, code)
                    return
                result_json = self.parse_query_result(rows)

                final_result = []
                for item in result_json:
                    snapshot = {
                        "instance": {
                            "uuid": item['basesnapshotinstanceno']
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

                message = self.create_response_message(code, "success", "", {"instance": final_result})
                self.send_response(message, code)

            except Exception as e:
                self.handle_exception(code, e)
        elif command == 'get':
            try:
                self.set_lastest_schema_rs()
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
                    message = self.create_response_message(code, "fail", "data not found", {})
                    self.send_response(message, code)
                    return

                message = self.create_response_message(code, "success", "", {"instance": final_result})
                self.send_response(message, code)

            except Exception as e:
                self.handle_exception(code, e)
        elif command == 'delete':
            try:
                api_client = self.api_client
                m = {
                    "request": {
                        "code": code,
                        "parameter": {
                            "command": command,
                            "data": data
                        }
                    }
                }
                res = api_client.modify_volume(m)
                res_dict = json.loads(res)

                response_key = next((key for key in res_dict.keys() if key.endswith('Response')), None)
                if response_key:
                    if 'blockStorageInstanceList' in res_dict[response_key]:
                        storage_list = res_dict[response_key]['blockStorageInstanceList']
                    elif 'blockStorageSnapshotInstanceList' in res_dict[response_key]:
                        storage_list = res_dict[response_key]['blockStorageSnapshotInstanceList']
                    else:
                        raise ValueError("Unexpected API response format")
                else:
                    raise ValueError("No valid response key found")

                instance_volumes = []
                for refine_dict in storage_list:
                    # 추출된 정보를 딕셔너리에 저장
                    structured_data = {
                        "serverinstanceno": refine_dict.get('serverInstanceNo'),
                        "blockstorageinstanceno": refine_dict.get('blockStorageInstanceNo') or refine_dict.get(
                            'blockStorageSnapshotInstanceNo'),
                        "blockstoragesnapshotinstanceno": refine_dict.get('blockStorageSnapshotInstanceNo'),
                        "originalblockstorageinstanceno": refine_dict.get('originalBlockStorageInstanceNo')
                    }

                    # 스냅샷 또는 볼륨 정보 구성
                    info = {
                        "uuid": structured_data["blockstorageinstanceno"],
                        "name": refine_dict.get('blockStorageName') or refine_dict.get('blockStorageSnapshotName'),
                        "type": refine_dict.get('blockStorageDiskDetailType', {}).get('codeName') or refine_dict.get(
                            'snapshotType', {}).get('codeName'),
                        "size": refine_dict.get('blockStorageSize') or refine_dict.get(
                            'blockStorageSnapshotVolumeSize'),
                        "status": refine_dict.get('blockStorageInstanceStatusName') or refine_dict.get(
                            'blockStorageSnapshotInstanceStatusName'),
                        "snapshot": None if command != 'create_snapshot' else structured_data[
                            "blockstoragesnapshotinstanceno"],
                        "raw": refine_dict
                    }

                    # code가 'snapshotinfo'일 경우 'snapshot'으로, 그 외의 경우 'volume'으로 키 설정
                    key = 'snapshot' if code == 'snapshotinfo' else 'volume'
                    instance_volumes.append({
                        key: info
                    })

                message = self.create_response_message(code, "success", "", {
                    "instance_volume": instance_volumes
                })
                self.send_response(message, code)

            except Exception as e:
                self.handle_exception(code, e)
        elif command == 'create':
            try:
                api_client = self.api_client
                m = {
                    "request": {
                        "code": code,
                        "parameter": {
                            "command": command,
                            "data": data
                        }
                    }
                }
                print(m)
                res = api_client.modify_volume(m)
                res_dict = json.loads(res)

                response_key = next((key for key in res_dict.keys() if key.endswith('Response')), None)
                # print(response_key)
                if response_key:
                    if 'blockStorageInstanceList' in res_dict[response_key]:
                        storage_list = res_dict[response_key]['blockStorageInstanceList']
                    elif 'blockStorageSnapshotInstanceList' in res_dict[response_key]:
                        storage_list = res_dict[response_key]['blockStorageSnapshotInstanceList']
                    else:
                        raise ValueError("Unexpected API response format")
                else:
                    raise ValueError("No valid response key found")

                instance_volumes = []
                for refine_dict in storage_list:
                    # 추출된 정보를 딕셔너리에 저장
                    # print(refine_dict)
                    structured_data = {
                        "serverinstanceno": refine_dict.get('serverInstanceNo'),
                        "blockstorageinstanceno": refine_dict.get('blockStorageInstanceNo') or refine_dict.get(
                            'blockStorageSnapshotInstanceNo'),
                        "blockstoragesnapshotinstanceno": refine_dict.get('blockStorageSnapshotInstanceNo'),
                        "originalblockstorageinstanceno": refine_dict.get('originalBlockStorageInstanceNo')
                    }

                    # 볼륨 정보 구성
                    volume_info = {
                        "uuid": structured_data["blockstorageinstanceno"],
                        "name": refine_dict.get('blockStorageName') or refine_dict.get('blockStorageSnapshotName'),
                        "type": refine_dict.get('blockStorageDiskDetailType', {}).get('codeName') or refine_dict.get(
                            'snapshotType', {}).get('codeName'),
                        "size": refine_dict.get('blockStorageSize') or refine_dict.get(
                            'blockStorageSnapshotVolumeSize'),
                        "status": refine_dict.get('blockStorageInstanceStatusName') or refine_dict.get(
                            'blockStorageSnapshotInstanceStatusName'),
                        "snapshot": None if command != 'create_snapshot' else structured_data[
                            "blockstoragesnapshotinstanceno"],
                        "raw": refine_dict
                    }

                    instance_volumes.append({
                        "volume": volume_info
                    })

                message = self.create_response_message(code, "success", "", {
                    "instance_volume": instance_volumes
                })
                self.send_response(message, code)

            except Exception as e:
                self.handle_exception(code, e)
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
            return "success"

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
                m = self.create_response_message(req_code, "success", "", {"resource": {"raw": res}})
                self.send_response(m, req_code)
            except Exception as e:
                self.handle_exception(req_code, e)
        elif command == 'delete':
            try:
                # detail_db_schema 스키마에 저장할 데이터 추출
                # resource_data = data.get('instance', [])
                resource_data = data.get('resource')
                api_client = self.api_client
                res = api_client.set_resource_info(resource_data)

                message = self.create_response_message(req_code, "success", "", {"resource": {"raw": res}})
                self.send_response(message, req_code)
            except Exception as e:
                self.handle_exception(req_code, e)
        elif command == 'set':
            try:
                # detail_db_schema 스키마에 저장할 데이터 추출
                # resource_data = data.get('instance', [])
                resource_data = data.get('resource')
                api_client = self.api_client
                res = api_client.set_resource_info(resource_data)
                message = self.create_response_message(req_code, "success", "", {"resource": {"raw": res}})
                self.send_response(message, req_code)
            except Exception as e:
                self.handle_exception(req_code, e)
        elif command == 'update':
            try:
                # recovery 데이터에서 필요한 정보 추출
                plan_info_list = data['plan']['instance']  # instance 리스트를 가져옴
                recovery_data = data['recovery']['raw']

                table_name = recovery_data['table_name']
                column_name = recovery_data['column_name']
                new_value = recovery_data['new_value']

                # 타겟 DB에 접속해서 가장 최신 스키마에 대해 raw SQL 실행
                schemas = self.execute_query_des("show schemas;")
                last_schema = next(
                    (schema['schema_name'] for schema in schemas if schema['schema_name'].startswith('rs_')), None)
                if last_schema is None:
                    last_schema = 'public'  # Default schema if none found

                # instance 리스트에 대해 반복
                for plan_info in plan_info_list:
                    uuid_value = plan_info['uuid']
                    res = self.update_column_by_id(last_schema, table_name, column_name, uuid_value, new_value)

                    # 각 instance에 대한 응답 메시지 생성 및 전송 (recoveryinfo 코드 사용)
                    message = self.create_response_message(req_code, "success", "",
                                                           {
                                                               "resource": f"table name: {table_name}, column name: {column_name}, old_value: {uuid_value}, new_value: {new_value}"}
                                                           )
                self.send_response(message, req_code)
            except Exception as e:
                self.handle_exception(req_code, e)

    def RecoveryInfo(self, command, data):
        code = "recoveryinfo"

        if command == 'get' or command == 'status':
            cmd = command
            try:
                plan_query = f'''SELECT * FROM {self.recovery_db_schema}.recoveryplan'''
                result_query = f'''SELECT * FROM {self.recovery_db_schema}.recoveryresults'''

                # self.execute_query_des()
                plan_res = self.execute_query_des(plan_query)
                result_res = self.execute_query_des(result_query)

                pdict = {}
                rlist = []

                # Retrieve the targetkey from the data['plan'] field(0910수정)
                target_k = data['plan']['instance'][0]['uuid']
                target_key = []
                for result in result_res:
                    target_key.append(result['targetkey'])

                for plan in plan_res:
                    source_key = plan['sourcekey']
                    # print(source_key)
                    # print(target_key)
                    #(0910수정)
                    if target_k in target_key:
                        tmp_query = f'''SELECT serverinstanceno, servername 
                                        FROM {self.detail_db_schema}.serverinstance 
                                        WHERE serverinstanceno = '{source_key}'
                                    '''
                        tmp_q_res = self.execute_query_des(tmp_query)
                        tmp_res = []

                    # tmp_query = f'''SELECT serverinstanceno, servername FROM {self.detail_db_schema}.serverinstance 
                    # WHERE serverinstanceno = '{source_key}'
                    # '''
                    # tmp_q_res = self.execute_query_des(tmp_query)
                    # tmp_res = []
                    for tq in tmp_q_res:
                        tmp_m = {
                            "uuid": tq['serverinstanceno'],
                            "name": tq['servername']
                        }
                        tmp_res.append(tmp_m)

                    result_entry = next((res for res in result_res if res['sourcekey'] == source_key), None)
                    if result_entry:
                        status_value = result_entry.get('status', '')
                        raw_value = result_entry.get('detail', '{}')
                    else:
                        status_value = ""
                        raw_value = {}

                    m = {
                        "id": plan['id'],
                        "name": plan['requestid'],
                        "instance": tmp_res
                    }
                    m1 = {
                    "status": status_value,
                    "raw": raw_value
                    }
                    # 0903 수정
                    # if 'plan' in data:
                    #     if plan['id'] == data['plan'].get('id'):
                    #         pdict[f"plan {plan['id']}"] = m  # 각 계획을 고유 키로 저장
                    # else:
                    #     pdict[f"plan {plan['id']}"] = m  # 각 계획을 고유 키로 저장

                    if 'plan' in data:
                        if plan['id'] == data['plan'].get('id'):
                            pdict[f"plan"] = m  # 각 계획을 고유 키로 저장
                            pdict["recovery"] = m1
                    else:
                        pdict[f"plan"] = m  # 각 계획을 고유 키로 저장
                        pdict["recovery"] = m1

                message = self.create_response_message(code, "success", "", pdict)
                self.send_response(message, code)

            except Exception as e:
                self.handle_exception(cmd, e)
        elif command == 'update':
            try:
                # recovery 데이터에서 필요한 정보 추출
                plan_info_list = data['plan']['instance']  # instance 리스트를 가져옴
                recovery_data = data['recovery']['raw']

                table_name = recovery_data['table_name']
                column_name = recovery_data['column_name']
                new_value = recovery_data['new_value']

                # 타겟 DB에 접속해서 가장 최신 스키마에 대해 raw SQL 실행
                schemas = self.execute_query_des("show schemas;")
                last_schema = next(
                    (schema['schema_name'] for schema in schemas if schema['schema_name'].startswith('ds_')), None)
                if last_schema is None:
                    last_schema = 'public'  # Default schema if none found

                # instance 리스트에 대해 반복
                for plan_info in plan_info_list:
                    uuid_value = plan_info['uuid']
                    res = self.update_column_by_id(last_schema, table_name, column_name, uuid_value, new_value)

                    tmp_query = f'''SELECT * FROM {self.detail_db_schema}.{table_name}'''
                    tmp_q_res = self.execute_query_des(tmp_query)

                    serializable_result = [self.convert_to_json(row) for row in tmp_q_res]

                    # 각 instance에 대한 응답 메시지 생성 및 전송 (recoveryinfo 코드 사용)
                    message = self.create_response_message('recoveryinfo', "success", "",
                                                           {
                                                               "raw": serializable_result,
                                                               "detail": f"table name: {table_name}, column name: {column_name}, old_value: {uuid_value}, new_value: {new_value}"}
                                                           )
                self.send_response(message, 'recoveryinfo')
            except Exception as e:
                self.handle_exception(code, e)
        # elif command == 'set':
            # try:
            #     recovery_info = data['plan']['raw']
            #     query = f"""
            #         INSERT INTO {self.db_database}.recovery.recoveryplan (id, requestid, resourcetype, sourcekey, "timestamp", command, detail, completeflag)
            #         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            #     """
            #     values = (
            #         recovery_info['requestid'], recovery_info['requestname'],recovery_info['resourcetype'], recovery_info['sourcekey'],
            #         recovery_info['timestamp'],
            #         recovery_info['command'], recovery_info['detail'], recovery_info['completeflag'])
            #     print(values)
                
            #     self.query_dbv2(query, values)
            #     message = self.create_response_message(code, "success", "", {})
            #     self.send_response(message, code)
            # except Exception as e:
            #     self.handle_exception(code, e)
        # 1024
        elif command == 'set':
            try:
                query = f"""
                    INSERT INTO {self.db_database}.recovery.recoveryplan (id, requestid, resourcetype, sourcekey, "timestamp", command, detail, completeflag)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    data['plan']['id'],
                    data['plan']['name'],
                    'serverinstance',
                    data['plan']['instance'][0]['uuid'],
                    str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                    "CREATE",
                    f"\"{data['plan']['instance'][0]['name']}\"",
                    'False'
                )   
                # print(values)
                self.query_dbv2(query, values)
                message = self.create_response_message(code, "success", "", {})
                self.send_response(message, code)
            except Exception as e:
                self.handle_exception(code, e)

        elif command == 'delete':
            try:
                plan_id = data['plan']['id']  # Extract the plan ID to delete

                # Delete from recoveryplan table
                delete_plan_query = f'''
                        DELETE FROM {self.recovery_db_schema}.recoveryplan 
                        WHERE id = %s
                    '''
                self.query_dbv2(delete_plan_query, (plan_id,))

                message = self.create_response_message(code, "success", "",
                                                       {"result": f"Plan id: {plan_id} deleted successfully"})
                self.send_response(message, code)

            except Exception as e:
                self.handle_exception(code, e)  # Handle potential errors

    def RecoveryJob(self, command, data):
        code = "recoveryjob"
        cmd = command
        # if command == 'run':
        #     try:
        #         print()
        #         ac = self.api_client
        #         endpoint = "recovery_vpc"
        #         # data = data['instance']
        #         res = ac.send_to_endpoint(endpoint, data)
        #         message = self.create_response_message(code, "success", "", data)
        #         self.send_response(message, code)
        #     except Exception as e:
        #         self.handle_exception(code, e)
        # 1024종우수정
        if command == 'run':
            try:
                try:
                    apiclientinrun = self.api_client
                    res = apiclientinrun.create_vpc()
                    test_API_request = self.create_response_message(code, "success", ":", data)
                except Exception as e:
                    test_API_request = self.create_response_message(code, "fail", str(f"Exception Code: {code}, E: {e}"), {})
       
                # test_API_request = "Exception: [ERR] No recoveryplan data found"

                # test_API_request = {
                #     "createServerInstancesResponse": {
                #         "requestId": "3b6fdb3a-ea15-4156-acb9-bb1004daecb7",
                #         "returnCode": "0",
                #         "returnMessage": "success",
                #         "serverInstanceList": [
                #             {
                #                 "baseBlockStorageDiskDetailType": {
                #                     "code": "SSD",
                #                     "codeName": "SSD"
                #                 },
                #                 "baseBlockStorageDiskType": {
                #                     "code": "NET",
                #                     "codeName": "\ub124\ud2b8\uc6cd \uc2a4\ud1a0\ub9ac\uc9c0"
                #                 },
                #                 "cpuCount": 2,
                #                 "createDate": "2024-10-24T21:30:36+0900",
                #                 "hypervisorType": {
                #                     "code": "XEN",
                #                     "codeName": "XEN"
                #                 },
                #                 "initScriptNo": "",
                #                 "isProtectServerTermination": 'false',
                #                 "loginKeyName": "k18cd8819c39",
                #                 "memberServerImageInstanceNo": "",
                #                 "memorySize": 4294967296,
                #                 "networkInterfaceNoList": [],
                #                 "placementGroupName": "",
                #                 "placementGroupNo": "",
                #                 "platformType": {
                #                     "code": "UBS64",
                #                     "codeName": "Ubuntu Server 64 Bit"
                #                 },
                #                 "publicIp": "",
                #                 "publicIpInstanceNo": "",
                #                 "regionCode": "KR",
                #                 "serverDescription": "",
                #                 "serverImageNo": "1700975",
                #                 "serverImageProductCode": "SW.VSVR.OS.LNX64.UBNTU.SVR2004.B050",
                #                 "serverInstanceNo": "100317147",
                #                 "serverInstanceOperation": {
                #                     "code": "NULL",
                #                     "codeName": "\uc11c\ubc84 NULL OP"
                #                 },
                #                 "serverInstanceStatus": {
                #                     "code": "INIT",
                #                     "codeName": "\uc11c\ubc84 INIT \uc0c1\ud0dc"
                #                 },
                #                 "serverInstanceStatusName": "init",
                #                 "serverInstanceType": {
                #                     "code": "HICPU",
                #                     "codeName": "High CPU"
                #                 },
                #                 "serverName": "vs192be81c8bb",
                #                 "serverProductCode": "SVR.VSVR.HICPU.C002.M004.NET.SSD.B050.G002",
                #                 "serverSpecCode": "c2-g2-s50",
                #                 "subnetNo": "",
                #                 "uptime": "2024-10-24T21:30:36+0900",
                #                 "vpcNo": "",
                #                 "zoneCode": "KR-1"
                #             }
                #         ],
                #         "totalRows": 1
                #     }
                # }

                if isinstance(test_API_request, dict) == False:
                    fail = test_API_request
                    message = self.create_response_message(code, "fail", fail, data)
                    self.send_response(message, code)

                elif test_API_request['createServerInstancesResponse']['returnMessage'] == "success":
                    message = self.create_response_message(code, "success", "", data)
                    self.send_response(message, code)


            except Exception as e:
                self.handle_exception(code, e)

        elif command == 'pause':
            try:
                message = self.create_response_message(code, "fail", "", "nothing to do")
                self.send_response(message, code)
            except Exception as e:
                self.handle_exception(code, e)

        elif command == 'stop':
            try:
                print("Stopping recovery job...")
                ac = self.api_client
                endpoint = "cancel_recovery_vpc"
                plan_id = data['plan']['id']
                stop_data = {'planid': plan_id}
                res = ac.send_to_endpoint(endpoint, stop_data)
                print('##>>',res)

                message = self.create_response_message(code, "success", "", data)
                self.send_response(message, code)
            except Exception as e:
                self.handle_exception(code, e)

        elif command == 'rollback':
            try:
                print()
                ac = self.api_client
                endpoint = "delete_vpc"
                # print(">>>",data)
                planid = data['plan']['id']
                # res = ac.send_to_endpoint(endpoint, data)
                # message = self.create_response_message(code, "success", "", res)

                recoveryplan_query = f"SELECT * FROM {self.recovery_db_schema}.recoveryplan WHERE completeflag=true AND id={planid};"
                recoveryplan_list = self.execute_query(recoveryplan_query)

                if recoveryplan_list:
                    for recoveryplan_table in recoveryplan_list:
                        resourceType = recoveryplan_table[2]
                        sourceKey = recoveryplan_table[3]
                        tmp_result_qry = (f"SELECT * FROM {self.recovery_db_schema}.recoveryresults WHERE sourcekey='{sourceKey}' AND resourcetype='{resourceType}';")
                        tmp_result_res = self.execute_query(tmp_result_qry)

                        if tmp_result_res:
                            for r in tmp_result_res:
                                tmp_table_name = r[2]
                                tmp_table_target_key = r[3]

                                ac = self.api_client
                                # ep = "delete_vpc"
                                # data = {
                                #     "delete": {
                                #         "target": tmp_table_name,
                                #         "body": {
                                #             f"{tmp_table_name}no": tmp_table_target_key
                                #         }
                                #     }
                                # }
                                # res = ac.send_to_endpoint(ep, data)

                                # if resource = serverinstance
                                # 1. stopServerInstances
                                tmp_url1 = f"/vserver/v2/stopServerInstances?regionCode=KR&serverInstanceNoList.1={tmp_table_target_key}"
                                tmp_res1 = ac.execute_resp(tmp_url1)

                                time.sleep(5) # waiting to stop

                                # 2. terminateServerInstances
                                tmp_url2 = f"/vserver/v2/terminateServerInstances?regionCode=KR&serverInstanceNoList.1={tmp_table_target_key}"
                                tmp_res2 = ac.execute_resp(tmp_url2)
                                # print(tmp_res2)

                        message = self.create_response_message(code, "success", "", "")
                else:
                    message = self.create_response_message(code, "fail", "data not found", "")
                self.send_response(message, code)
            except Exception as e:
                self.handle_exception(code, e)
