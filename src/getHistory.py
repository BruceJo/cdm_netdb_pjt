import json
import requests
import hmac
import hashlib
import base64
import time


class Tracer():
    def __init__(self, api):
        self.http_url = 'https://cloudactivitytracer.apigw.gov-ntruss.com'
        self.api_url = '/api/v1/activities'
        self.secret_key = api['secretKey']
        self.access_key = api['accessKey']

    # conn api
    def create_signature(self, timestamp):
        secret_key_bytes = bytes(self.secret_key, 'UTF-8')
        message = bytes(f"POST {self.api_url}\n{timestamp}\n{self.access_key}", 'UTF-8')
        signing_key = base64.b64encode(hmac.new(secret_key_bytes, message, digestmod=hashlib.sha256).digest())
        return signing_key
    
    def send_request(self):
        timestamp = str(int(time.time() * 1000))
        signature = self.create_signature(timestamp)
        print(type(signature))
        http_header = {
            'Content-Type': 'application/json; charset=utf-8',
            'x-ncp-apigw-timestamp': timestamp,
            'x-ncp-iam-access-key': self.access_key,
            'x-ncp-apigw-signature-v2': signature
        }
        print(http_header)
        # https://api-gov.ncloud-docs.com/docs/management-cloudactivitytracer-getactivitylist
        json_body = {
            # "fromEventTime": "integer",
            # "toEventTime": "integer",
            # "nrn": "string",
            # "pageIndex": "integer",
            "pageSize": "100"
        }
        response = requests.post(self.http_url + self.api_url, data=json.dumps(json_body), headers=http_header)
        print(response)
        result = json.loads(response.text)

        return result

class History():
    def __init__(self, target_api):
        self.target_api = target_api
        self.cc = Tracer(api=target_api)

    def run(self):
        # 0. app.conf에 1)새로고침 주기와 2)from~to의 간격 명시
        # 1. 오브젝트 file이 없다면 from~to 기간 조회해서 df를 만들고 오브젝트를 file로 저장
        # 2. 오브젝트 file이 있다면 from~to 기간 조회해서 df를 만들고 오브젝트를 file과 비교 (pk:historyId, rm:action!=Login)
        # 3. 이벤트의 productName, resourceType을 조합하고, historyDiffFlag==True 정보를 활용
            # 3.1 조합 정보와 테이블을 매핑
            # 3.2 변경된 정보가 여러개라면 업데이트 할 순서를 정해야함
            # 3.3 변경된 정보에 따라, 다른 테이블의 정보도 업데이트 될 수 있지않나?

        # 4. 비교했을 때 추가 생성된게 존재하면 해당 이벤트에 해당하는 자원을 새로 조회하여
            # 4.1 해당하는 자원의 기존 테이블을 업데이트 - 제일 베스트지만, 뭐
            # 4.2 해당하는 자원의 기존 테이블을 삭제하고 새로 삽입 - row가 항상 동일한 순서대로 삽입되면 seq.만 초기화하여 삽입 가능
            # 4.3 모든 기존 테이블을 삭제하고 새로 삽입 - 네버스탑에서 db상 id를 따로 추적(변경사항관리 등)하지 않는다면
        res = self.cc.send_request()

        return json.dumps(res)