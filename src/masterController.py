import pika
import json
import uuid

class MasterController:
    def __init__(self, hostname, port):
        self.test = "test"
        self.host = hostname
        self.port = port
        self.username = "admin"
        self.userpassword = "admin"
        self.request_queue = 'request_queue'
        self.response_queue = 'response_queue'

    def run(self):
        self.main_req()

    def send_request(self, request_queue, request_ID, request_message):
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.host, self.port, '/', pika.PlainCredentials(self.username, self.userpassword)))
        channel = connection.channel()
        channel.queue_declare(queue=request_queue)
        channel.basic_publish(exchange='', routing_key=request_queue, body=json.dumps(request_message))
        print(f"SEND {request_message} TO {request_queue} FOR {request_ID}")
        connection.close()

    def receive_response(self, response_queue, request_ID):
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.host, self.port, '/', pika.PlainCredentials(self.username, self.userpassword)))
        channel = connection.channel()
        channel.queue_declare(queue=response_queue)
        method_frame, header_frame, body = channel.basic_get(queue=response_queue, auto_ack=True)
        if method_frame:
            print(f"RECEIVED '{body}' FROM {response_queue} FOR {request_ID}")
            body = body.decode('utf-8')
            body = json.loads(body)
        else:
            print(f"No message in {response_queue}")
            connection.close()
            return None
        request_result = body
        print('Request_Result:')
        print(request_result)
        connection.close()
        return request_result

    def test_clusterinfo(self):
        request_ID = str(uuid.uuid4())
        request_message = {
            "request": {
                "id": request_ID,
                "code": "clusterinfo",
                "parameter": {
                    "command": "get",
                    "data": {}
                }
            }
        }
        self.send_request(self.request_queue, request_ID, request_message)
        self.receive_response(self.response_queue, request_ID)

    def test_instanceinfo(self):
        request_ID = str(uuid.uuid4())
        request_message = {
            "request": {
                "id": request_ID,
                "code": "instanceinfo",
                "parameter": {
                    "command": "get",
                    "data": {}
                }
            }
        }
        self.send_request(self.request_queue, request_ID, request_message)
        self.receive_response(self.response_queue, request_ID)

    def test_volumeinfo(self):
        request_ID = str(uuid.uuid4())
        request_message = {
            "request": {
                "id": request_ID,
                "code": "volumeinfo",
                "parameter": {
                    "command": "get",
                    "data": {}
                }
            }
        }
        self.send_request(self.request_queue, request_ID, request_message)
        self.receive_response(self.response_queue, request_ID)

    def test_snapshotinfo(self):
        request_ID = str(uuid.uuid4())
        request_message = {
            "request": {
                "id": request_ID,
                "code": "snapshotinfo",
                "parameter": {
                    "command": "get",
                    "data": {}
                }
            }
        }
        self.send_request(self.request_queue, request_ID, request_message)
        self.receive_response(self.response_queue, request_ID)

    def test_recoveryjob(self):
        request_ID = str(uuid.uuid4())
        request_message = {
            "request": {
                "id": request_ID,
                "code": "recoveryjob",
                "parameter": {
                    "command": "run",
                    "data": {}
                }
            }
        }
        self.send_request(self.request_queue, request_ID, request_message)
        self.receive_response(self.response_queue, request_ID)

    def test_resourceinfo(self):
        request_ID = str(uuid.uuid4())
        request_message = {
            "request": {
                "id": request_ID,
                "code": "resourceinfo",
                "parameter": {
                    "command": "get",
                    "data": {}
                }
            }
        }
        self.send_request(self.request_queue, request_ID, request_message)
        self.receive_response(self.response_queue, request_ID)

    def test_recoveryinfo(self):
        request_ID = str(uuid.uuid4())
        request_message = {
            "request": {
                "id": request_ID,
                "code": "recoveryinfo",
                "parameter": {
                    "command": "get",
                    "data": {}
                }
            }
        }
        self.send_request(self.request_queue, request_ID, request_message)
        self.receive_response(self.response_queue, request_ID)

    def main_req(self):
        self.test_clusterinfo()
        self.test_instanceinfo()
        self.test_volumeinfo()
        self.test_snapshotinfo()
        self.test_recoveryjob()
        self.test_resourceinfo()
        self.test_recoveryinfo()
