import pika
import json
import uuid
from Functions1 import Functions
from datetime import datetime
import apiClient


class MessageInterface:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials('admin', 'admin')))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='request_exchange', exchange_type='topic')
        self.channel.exchange_declare(exchange='response_exchange', exchange_type='topic')
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.queue_bind(exchange='request_exchange', queue=self.callback_queue, routing_key='common')
        self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.on_request, auto_ack=True)

    def on_request(self, ch, method, props, body):
        request = json.loads(body)
        print(f"Received request: {request}")

        # process_request 함수를 먼저 적용
        processed_request = self.process_request(request)

        # Functions 클래스의 receive_request 메서드 호출
        functions = Functions(processed_request['request_ID'])
        response = functions.receive_request()

        self.channel.basic_publish(
            exchange='response_exchange',
            routing_key='common',
            body=json.dumps(response)
        )
        print(f"Sent response: {response}")

    def run(self):
        print('Waiting for requests. To exit press CTRL+C')
        self.channel.start_consuming()

    def process_request(self, request):
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
            if "instance_volume" in request['request']['parameter']['data'] and "uuid" in \
                    request['request']["parameter"]["data"]["instance_volume"][0]["instance"]:
                request_uuid = request['request']["parameter"]["data"]["instance_volume"][0]["instance"]["uuid"]
            else:
                request_command = "get_all"
        elif request_code == "snapshotinfo" and request_command == "get":
            if "instance" in request['request']['parameter']['data'] and "uuid" in request['request']['parameter']['data'][
                'instance']:
                request_uuid = request['request']["parameter"]["data"]["instance"]["uuid"]
            else:
                request_command = "get_all"

        request_message = {
            'request_ID': request_ID,
            'request_code': request_code,
            'request_command': request_command,
            'request_data': request_data
        }

        return request_message

if __name__ == "__main__":
    interface = MessageInterface()
    interface.run()