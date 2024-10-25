import time
import json
import base64
import hashlib
import hmac
import requests


class ApiClient:
    def __init__(self):
        config = {
            'ip': 'localhost',
            'api_source': {
                'accessKey': 'mYUP1ZqESUOpjyOokWC8',
                'secretKey': '31scunD8FAtSTqU92X2DYFsi1UaiEbQ5qrTxi2aM',
                'ncloudUrl': 'https://ncloud.apigw.gov-ntruss.com',
                'billingApiUrl': 'https://billingapi.apigw.gov-ntruss.com'
            },
            'dbSource': {
                'dbName': 'cdm_fix',
                'schemaName': 'test240925t',
                'host': '175.45.214.45',
                'port': '26257',
                'user': 'root'
            }
        }
        self.base_url = f"http://{config['ip']}:9999"
        self.api_source = config['api_source']
        self.database = config['dbSource']
        self.headers = {
             "Accept": "*/*",
             "User-Agent": "Thunder Client (https://www.thunderclient.com)",
              "Content-Type": "application/json"
        }

    def create_schema(self):
        data = {
            "dbName": self.database["dbName"],
            "schemaName": self.database["schemaName"],
            "host": self.database["host"],
            "port": self.database["port"],
            "user": self.database["user"]
        }
        payload = json.dumps(data)
        response = requests.post(f"{self.base_url}/create_schema", data=payload, headers=self.headers)
        return response.text

    def create_recovery(self):
        response = requests.post(f"{self.base_url}/create_recovery", data={}, headers=self.headers)
        return response.text

    def set_resource_info(self, data):
        # payload = json.dumps(data)
        payload = data
        response = requests.post(f"{self.base_url}/set_resource_info", data=payload, headers=self.headers)
        return response.text

    def set_recovery_info(self, data):
        payload = json.dumps(data)
        # payload = data
        response = requests.post(f"{self.base_url}/set_recovery_info", data=payload, headers=self.headers)
        return response.text

    def source_to_target(self):
        data = {}
        payload = json.dumps(data)
        response = requests.post(f"{self.base_url}/source_to_target", data={}, headers=self.headers)
        return response.text

    def get_resource_list(self):
        data = {}
        payload = json.dumps(data)
        response = requests.post(f"{self.base_url}/get_resource_list", data=payload, headers=self.headers)
        return response.text

    def sync_cluster(self):
        data = {}
        payload = json.dumps(data)
        response = requests.post(f"{self.base_url}/sync_cluster", data=payload, headers=self.headers)
        return response.text

    def read2insert(self):
        data = {
            "apiSource": self.api_source,
            "dbSource": {
                "dbName": self.database["dbName"],
                "schemaName": self.database["schemaName"],
                "schemaPath": "../schema/naverCloudSchema.sql",
                "host": self.database["host"],
                "port": self.database["port"],
                "user": self.database["user"]
            }
        }
        payload = json.dumps(data)
        response = requests.post(f"{self.base_url}/read2insert", data=payload, headers=self.headers)
        return response.text

    def recovery_vpc(self):
        if self.api_source is None or self.database is None:
            return "API source or database configuration is missing."

        data = {
            "apiSource": self.api_source,
            "dbSource": {
                "dbName": self.database["dbName"],
                "schemaName": self.database["schemaName"],
                "schemaPath": "../schema/naverCloudSchema.sql",
                "host": self.database["host"],
                "port": self.database["port"],
                "user": self.database["user"]
            }
        }
        payload = json.dumps(data)
        response = requests.post(f"{self.base_url}/recovery_vpc", data=payload, headers=self.headers)
        return response.text

    def modify_volume(self, data):
        payload = json.dumps(data)
        response = requests.post(f"{self.base_url}/modify_volume", data=payload, headers=self.headers)
        return response.text

    def reboot_serverinstances(self, data):
        payload = json.dumps(data)
        response = requests.post(f"{self.base_url}/reboot_serverinstances", data=payload, headers=self.headers)
        return response.text

    def send_to_endpoint(self, endpoint, data):
        payload = json.dumps(data)
        response = requests.post(f"{self.base_url}/{endpoint}", data=payload, headers=self.headers)
        return response.text

    def execute_resp(self, api_url):
        response = self.send_request("GET", api_url, str(int(time.time() * 1000)))
        # response = requests.get(f"{self.base_url}/{self.api_url}", headers=self.headers)
        print("##>>",response.text)
        return response.text

    def create_signature(self, method, api_url, timestamp, access_key):
        message = f"{method} {api_url}\n{timestamp}\n{access_key}"
        print(f"###\n\n\n{message}\n\n\n###")
        message = bytes(message, 'UTF-8')
        SECRET_KEY = self.api_source['secretKey']
        secret_key_bytes = bytes(SECRET_KEY, 'UTF-8')

        signing_key = base64.b64encode(hmac.new(secret_key_bytes, message, digestmod=hashlib.sha256).digest())
        return signing_key

    def send_request(self, method, api_url, timestamp):
        ACCESS_KEY = self.api_source['accessKey']
        signature = self.create_signature(method, api_url, timestamp, ACCESS_KEY)
        http_header = {
            'x-ncp-apigw-timestamp': timestamp,
            'x-ncp-iam-access-key': ACCESS_KEY,
            'x-ncp-apigw-signature-v2': signature
        }
        full_url = self.api_source['ncloudUrl'] + api_url
        print("full_url is ::", full_url)
        response = requests.get(full_url, headers=http_header)
        return response
    
    def create_vpc(self):
        if self.api_source is None or self.database is None:
            return "API source or database configuration is missing."

        data = {
            "apiSource": self.api_source,
            "dbSource": {
                "dbName": self.database["dbName"],
                "schemaName": self.database["schemaName"],
                "schemaPath": "../schema/naverCloudSchema.sql",
                "host": self.database["host"],
                "port": self.database["port"],
                "user": self.database["user"]
            }
        }
        
        payload = json.dumps(data)
        response = requests.post(f"{self.base_url}/create_vpc", data=payload, headers=self.headers)
        return response.text




if __name__ == '__main__':
    #src
    config1 = {
        'ip': 'localhost', # API Server IPaddr
        'api_source': {
            'accessKey': 'mYUP1ZqESUOpjyOokWC8',
            'secretKey': '31scunD8FAtSTqU92X2DYFsi1UaiEbQ5qrTxi2aM',
            'ncloudUrl': 'https://ncloud.apigw.gov-ntruss.com',
            'billingApiUrl': 'https://billingapi.apigw.gov-ntruss.com'
        },
        'dbSource': {
            'dbName': 'cdm_fix', # API Server IPaddr
            'schemaName': 'test240925t',
            'host': '175.45.214.45',
            'port': '26257',
            'user': 'root'
        }
    }
    #tgt
    config2 = {
        'ip': 'localhost',
        'api_source': {
            'accessKey': '9AB413B39F22F35B57BD',
            'secretKey': 'E2B9D2670DCB51B93A595E75D21140771105C1E0',
            'ncloudUrl': 'https://ncloud.apigw.gov-ntruss.com',
            'billingApiUrl': 'https://billingapi.apigw.gov-ntruss.com'
        },
        'dbSource': {
            'dbName': 'cdm_fix',
            'schemaName': 'test240925t',
            'host': '175.45.214.45',
            'port': '26257',
            'user': 'root'
        }
    }
    src_client = ApiClient()
    src_client.sync_cluster()
    # tgt_client = ApiClient(config2)