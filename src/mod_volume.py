import base64
import hashlib
import hmac
import time
import requests
import getConfig as gcf


class volume_control:
    def __init__(self, command, serverinstanceno=None, volumeinstanceno=None, default_ip="localhost"):
        self.status_path = "../conf/status.conf"
        self.config_path = "../conf/app.conf"
        self.db_temp_path = "./db_temp.pkl"
        self.api = gcf.Config(self.config_path).getConfig()['API-SOURCE-NAVER-CLOUD'].copy()
        self.base_url = f"http://{default_ip}:9999"
        self.headers = {
            "Accept": "*/*",
            "User-Agent": "Thunder Client (https://www.thunderclient.com)",
            "Content-Type": "application/json"
        }
        if command == "read":
            self.api_url = "/vserver/v2/getBlockStorageInstanceList"
        elif command == "create":
            self.api_url = f"/vserver/v2/createBlockStorageInstance?regionCode=KR&serverInstanceNo={serverinstanceno}&blockStorageSize=100"
        elif command == "attach":
            self.api_url = f"/vserver/v2/attachBlockStorageInstance?regionCode=KR&blockStorageInstanceNo={volumeinstanceno}&serverInstanceNo={serverinstanceno}"
        elif command == "detach":
            self.api_url = f"/vserver/v2/detachBlockStorageInstances?regionCode=KR&blockStorageInstanceNoList.1={volumeinstanceno}"
        elif command == "delete":
            self.api_url = f"/vserver/v2/deleteBlockStorageInstances?regionCode=KR&blockStorageInstanceNoList.1={volumeinstanceno}"
        elif command == "create_snapshot_volume":
            self.api_url = f"/vserver/v2/createBlockStorageSnapshotInstance?regionCode=KR&originalBlockStorageInstanceNo={volumeinstanceno}"
        elif command == "get_snapshot_volume":
            self.api_url = f"/vserver/v2/getBlockStorageSnapshotInstanceList?regionCode=KR"
        elif command == "delete_snapshot_volume":
            self.api_url = f"/vserver/v2/deleteBlockStorageSnapshotInstances?regionCode=KR&blockStorageSnapshotInstanceNoList.1={volumeinstanceno}"

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

