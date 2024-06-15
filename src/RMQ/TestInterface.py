import pika
import json
import uuid
from Functions1 import Functions
from datetime import datetime
import apiClient

class TestInterface:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials('admin', 'admin')))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='request_exchange', exchange_type='topic')
        self.channel.exchange_declare(exchange='response_exchange', exchange_type='topic')
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.queue_bind(exchange='response_exchange', queue=self.callback_queue, routing_key='#')
        self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.on_response, auto_ack=True)
        self.api_client = apiClient.ApiClient()

    def on_response(self, ch, method, props, body):
        self.response = json.loads(body.decode('utf-8'))

    def send_request(self, exchange, routing_key, request_message):
        request_message_str = json.dumps(request_message, indent=2)
        # print(f"SEND REQUEST MESSAGE:\n{request_message_str}")
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=json.dumps(request_message))
        # print(f"SEND {request_message} TO {exchange} WITH ROUTING_KEY {routing_key}")

    def receive_response(self):
        self.response = None
        while self.response is None:
            self.connection.process_data_events()
        response_str = json.dumps(self.response, indent=2)
        return self.response

    def close(self):
        self.connection.close()

    def test_resourceinfo(self):
        # ResourceInfo 함수 테스트
        request = create_request("resourceinfo", "get", {})
        response = self.test_message(request)
        # get 명령어 결과를 set 명령어로 전달하여 테스트
        # res to req

        if response['response']['code'] == 'resourceinfo' and response['response']['message'] == 'success':
            data = response['response']['data']['resource']
            request = create_request("resourceinfo", "set", {"resource": data})
            self.test_message(request)
        else:
            print("get command error")

    def test_message(self, request):
        request_exchange = 'request_exchange'
        response_exchange = 'response_exchange'

        request_message = process_request(request)
        self.send_request(request_exchange, 'common', request_message)

        Functions(request_message['request_ID']).receive_request()

        response = self.receive_response()
        print("응답 메시지:")
        return response


def create_request(code, command, data):
    m = {
        "request": {
            "id": str(uuid.uuid4()),
            "code": code,
            "parameter": {
                "command": command,
                "data": data
            }
        }
    }
    request_message_str = json.dumps(m, indent=2)
    print(f"request {code}.{command}\n{request_message_str}")
    return m


def process_request(request):
    # print("###")
    # print(request)
    request_ID = request['request']['id']
    request_code = request['request']['code']
    request_command = request['request']['parameter']['command']
    request_data = request['request']['parameter']['data']
    request_uuid = None

    if request_code == "instanceinfo" and request_command == "get":
        if "uuid" in request['request']['parameter']['data']:
            request_uuid = request['request']["parameter"]["data"]["uuid"]
        else:
            request_command = "get_all"
    elif request_code == "volumeinfo" and request_command == "get":
        if "instance" in request['request']['parameter']['data'] and "uuid" in request['request']['parameter']['data']['instance']:
            request_uuid = request['request']["parameter"]["data"]["instance"]["uuid"]
        else:
            request_command = "get_all"
    elif request_code == "snapshotinfo" and request_command == "get":
        if "instance" in request['request']['parameter']['data'] and "uuid" in request['request']['parameter']['data']['instance']:
            request_uuid = request['request']["parameter"]["data"]["instance"]["uuid"]
        else:
            request_command = "get_all"

    request_message = {
        'request_ID': request_ID,
        'request_code': request_code,
        'request_command': request_command,
        'request_data': request_data
    }

    if request_uuid is not None:
        request_message['request_data']['uuid'] = request_uuid

    return request_message


def test_message(request):
    request_exchange = 'request_exchange'
    response_exchange = 'response_exchange'

    interface = TestInterface()
    request_message = process_request(request)
    interface.send_request(request_exchange, 'common', request_message)

    Functions(request_message['request_ID']).receive_request()

    response = interface.receive_response()
    # print("응답 메시지:")
    # print(response)

    interface.close()


def test_clusterinfo():
    # request = create_request("clusterinfo", "get", {})
    # test_message(request)
    request = create_request("clusterinfo", "sync", {})
    test_message(request)


def test_instanceinfo():
    request = create_request("instanceinfo", "get", {"instance": [{"uuid": "3081226"}]})  # uuid for test
    test_message(request)
    #
    # request = create_request("instanceinfo", "get", {})
    # test_message(request)

    # request = create_request("instanceinfo", "reboot", {"instance": [
    #     {
    #         "uuid": '3081226'
    #     }
    # ]})
    # test_message(request)


def test_volume():
    # request = create_request("volumeinfo", "get", {"instance": [{"uuid": "2483886"}]})  # uuid for test
    # test_message(request)
    #
    # request = create_request("volumeinfo", "get", {"instance": []})
    # test_message(request)
    # request = create_request("volumeinfo", "create", {"instance": [{"uuid": "3081226"}]})
    request = create_request("volumeinfo", "delete", {"instance": [{"uuid": "3183443"}]})
    # request = create_request("volumeinfo", "detach", {"instance": [{"uuid": "3183443"}]})
    # request = create_request("volumeinfo", "create_snapshot_volume", {"instance": [{"uuid": "3081227"}]})
    # request = create_request("volumeinfo", "attach", {"instance": [{"volume_uuid": "3183443", "instance_uuid": "3081226"}]})

    # print(request)
    test_message(request)


def test_snapshot():
    # request = create_request("snapshotinfo", "get", {"instance": [
    #     {
    #         "instance": {"uuid": "2483886"},
    #         "volumeinfo": [{"uuid": "3456789", "snapshotinfo": [{"uuid": "1234567"}]}]
    #     }
    # ]})3160361
    # test_message(request)
    # request = create_request("snapshotinfo", "get", {"instance": []})
    request = create_request("snapshotinfo", "delete", {"instance": [{"uuid": "3183468"}]})

    test_message(request)




def test_resourceinfo():
    # request = create_request("resourceinfo", "get", {"instance": {}})
    # request = create_request("resourceinfo", "get", {"instance": {"uuid": ["1947812"]}})

    message_update = {
        "request": {
            "id": str(uuid.uuid4()),  # Generate a unique ID
            "code": "resourceinfo",
            "parameter": {
                "command": "update",
                "data": {
                    "plan": {
                        "id": 1,  # You can adjust this ID as needed
                        "name": "DR_DEMO_001",
                        "instance": [
                            {
                                "uuid": '3051792',
                                "name": 's18fb360bc62'
                            }
                        ]
                    },
                    "recovery": {
                        "raw": {
                            "table_name": "serverinstance",
                            "column_name": "servername",
                            "uuid": 1,
                            "new_value": "updated_name"
                        }
                    }
                }
            }
        }
    }

    request_message_str = json.dumps(message_update, indent=2)
    print(f"request \n{request_message_str}")

    # request = create_request("resourceinfo", "update", {"instance": [
    #     {
    #         "table_name": "serverinstance",
    #         "column_name": "servername",
    #         "uuid": 1,
    #         "new_value": "new_name"
    #     }
    # ]})
    # test_message(request)
    test_message(message_update)

def generate_recovery_info(requestid, resourcetype, sourcekey, command, detail=None, completeflag=False):
    recovery_info = {
        'requestid': requestid,
        'resourcetype': resourcetype,
        'sourcekey': sourcekey,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'command': command,
        'detail': detail,
        'completeflag': completeflag
    }
    m = {
        "plan": {
            "id": requestid,
            "name": requestid,
            "instance": [
                recovery_info
            ]
        }
    }
    return m
def test_recoveryinfo():
    # request = create_request("recoveryinfo", "get", {})
    # test_message(request)
    recovery_info = generate_recovery_info(
        requestid='DR_DEMO_001',
        resourcetype='serverinstance',
        sourcekey='3051792',  # target-contoller key
        command='CREATE',
        detail=None,
        completeflag=False
    )
    p = {"plan": {
        "id": 1,
        "name": "target-A"
    }}
    # request = create_request("recoveryinfo", "status", data=p)
    # request = create_request("recoveryinfo", "delete",  data=p)
    request = create_request("recoveryinfo", "set", recovery_info)


#
#     request = create_request("resourceinfo", "get", {"instance": {"uuid": ["1910516"]}})
#     test_message(request)
#
    # request = create_request("resourceinfo", "set", {"instance": instance_data})
    test_message(request)

def test_recoveryjob():
    req_code = 'recoveryjob'
    p = {"plan": {
        "id": 1,
        "name": "target-A"
    }}

    # request1 = create_request(req_code, "run", {"instance": p})
    # request2 = create_request(req_code, "pause", {"instance": p})
    # request3 = create_request(req_code, "stop", {"instance": p})
    request4 = create_request(req_code, "rollback", {"instance": p})

    test_message(request4)




if __name__ == "__main__":
    # test_clusterinfo()
    # test_instanceinfo()
    # print("테스트 완료 test_instanceinfo\n\n")
    # test_volume()
    # print("테스트 완료 test_volume\n\n")
    test_snapshot()
    # test_recoveryinfo()
    # print("테스트 완료 test_snapshot\n\n")
    # test_resourceinfo()
    # test_interface = TestInterface()
    # test_interface.api_client.create_recovery()
    # test_interface.test_resourceinfo()
    # test_recoveryjob()


    print("")
