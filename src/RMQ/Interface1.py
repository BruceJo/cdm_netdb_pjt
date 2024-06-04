import pika
import json
import sys
import io
from Functions1 import Functions


def __main__():
    # 메인 실행문
    request = {
        "request": {
            "id": "test_request_ID",  # 요청 메시지를 구분하기 위한 ID
            "code": "snapshot",  # code: request 요청 코드
            "parameter": {
                "command": "get",  # parameter.command: request 요청 동작
                "data": {
                    "instance": {
                        # "ukey": ["1"],  # 유니크 key
                    }
                }
            }
        }
    }

    request_ID = request['request']['id']  # UUID
    request_code = request['request']['code']  # code
    request_command = request['request']['parameter']['command']  # parameter.command
    request_ukey = ""
    if request_code == "instanceinfo":
        if "ukey" in request['request']['parameter']['data']:
            request_ukey = request['request']["parameter"]["data"]["ukey"]
        else:
            request_command = "get_all"
    elif request_code == "volume":
        if "ukey" in request['request']['parameter']['data']['instance']:
            request_ukey = request['request']["parameter"]["data"]["instance"]["ukey"]
        else:
            request_command = "get_all"
    elif request_code == "snapshot":
        if "ukey" in request['request']['parameter']['data']['instance']:
            request_ukey = request['request']["parameter"]["data"]["instance"]["ukey"]
        else:
            request_command = "get_all"

    request_message = {  # Functionals로 보낼 request_message
        'request_ID': request_ID,
        'request_code': request_code,
        'request_command': request_command,
        'request_ukey': request_ukey
    }

    request_exchange = 'request_exchange'  # request 메시지 넣는 exchange 이름
    response_exchange = 'response_exchange'  # response 메시지 넣는 exchange 이름

    # Interface에서 send_request는 요청 메시지 전송 / receive_response는 응답 메시지 받기
    # 메세지 송수신은 비동기입니다(사용자 설정 필요)
    # 이부분 에서 송신 또는 수신 설정하기
    interface = Interface()
    interface.send_request(request_exchange, 'common', request_message)
    Functions(request_ID).receive_request()  # Functions에서 receive_request 함수 실행
    interface.receive_response(response_exchange, request_code, request_ID)


class Interface:
    # 인터페이스 클래스

    def __init__(self):
        # 전역변수 정리
        self.test = "test"

    def send_request(self, exchange, routing_key, request_message):
        # Functionals로 request 전송
        connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials('admin', 'admin')))
        channel = connection.channel()
        channel.exchange_declare(exchange=exchange, exchange_type='topic')
        channel.basic_publish(exchange=exchange, routing_key=routing_key, body=json.dumps(request_message))
        print(f"SEND {request_message} TO {exchange} WITH ROUTING_KEY {routing_key}")
        connection.close()

    def receive_response(self, exchange, routing_key, request_ID):
        # response_queue에서 response_message 받기
        connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials('admin', 'admin')))
        channel = connection.channel()
        channel.exchange_declare(exchange=exchange, exchange_type='topic')
        result = channel.queue_declare(queue='response_queue', exclusive=False)
        queue_name = result.method.queue
        channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=routing_key)

        def callback(ch, method, properties, body):
            print(f"RECEIVED '{body}' FROM {exchange} WITH ROUTING_KEY {routing_key} FOR {request_ID}")
            body = body.decode('utf-8')
            body = json.loads(body)
            request_result = body
            print('Request_Result: ')
            print(request_result)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            ch.stop_consuming()  # 메시지 수신 후 소비 중단

        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)
        # print(f"Waiting for messages in {queue_name} with routing key {routing_key}")
        channel.start_consuming()


if __name__ == "__main__":
    __main__()
