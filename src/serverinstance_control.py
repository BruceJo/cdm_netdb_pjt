import base64
import hashlib
import hmac
import time
import requests
import getConfig as gcf


class serverinstance_control:
    def __init__(self, command, serverinstance_list, default_ip="localhost"):
        self.status_path = "../conf/status.conf"
        self.config_path = "../conf/app.conf"
        self.db_temp_path = "./db_temp.pkl"
        self.api = gcf.Config(self.config_path).getConfig()['API-SOURCE-NAVER-CLOUD'].copy()
        print(">>>",self.api)
        self.base_url = f"http://{default_ip}:9999"
        self.headers = {
            "Accept": "*/*",
            "User-Agent": "Thunder Client (https://www.thunderclient.com)",
            "Content-Type": "application/json"
        }
        if command == "reboot":
            self.api_url = "/vserver/v2/rebootServerInstances?regionCode=KR"
            for i, server_instance_no in enumerate(serverinstance_list):
                server_instance_no = int(server_instance_no)
                param = f"serverInstanceNoList.{i + 1}={server_instance_no}"
                if "?" in self.api_url:  # 이미 쿼리 파라미터가 있는 경우
                    self.api_url += f"&{param}"
                else:  # 쿼리 파라미터가 없는 경우
                    self.api_url += f"?{param}"

    def execute_resp(self):
        response = self.send_request("GET", self.api_url, str(int(time.time() * 1000)))
        # response = requests.get(f"{self.base_url}/{self.api_url}", headers=self.headers)
        print("##>>",response.text)
        return response.text

    def create_signature(self, method, api_url, timestamp, access_key):
        message = f"{method} {api_url}\n{timestamp}\n{access_key}"
        print(f"###\n\n\n{message}\n\n\n###")
        message = bytes(message, 'UTF-8')
        SECRET_KEY = self.api['secretKey']
        secret_key_bytes = bytes(SECRET_KEY, 'UTF-8')

        signing_key = base64.b64encode(hmac.new(secret_key_bytes, message, digestmod=hashlib.sha256).digest())
        return signing_key

    def send_request(self, method, api_url, timestamp):
        ACCESS_KEY = self.api['accessKey']
        signature = self.create_signature(method, api_url, timestamp, ACCESS_KEY)
        http_header = {
            'x-ncp-apigw-timestamp': timestamp,
            'x-ncp-iam-access-key': ACCESS_KEY,
            'x-ncp-apigw-signature-v2': signature
        }
        full_url = self.api['ncloudUrl'] + api_url
        print("full_url is ::", full_url)
        response = requests.get(full_url, headers=http_header)
        return response

