import requests
import json


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
                  'schemaName': 'test',
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

if __name__ == '__main__':
    #src
    config1 = {
        'ip': '175.45.214.45',
        'api_source': {
            'accessKey': 'mYUP1ZqESUOpjyOokWC8',
            'secretKey': '31scunD8FAtSTqU92X2DYFsi1UaiEbQ5qrTxi2aM',
            'ncloudUrl': 'https://ncloud.apigw.gov-ntruss.com',
            'billingApiUrl': 'https://billingapi.apigw.gov-ntruss.com'
        },
        'dbSource': {
            'dbName': 'cdm_fix',
            'schemaName': 'test',
            'host': '175.45.214.45',
            'port': '26257',
            'user': 'root'
        }
    }
    #tgt
    config2 = {
        'ip': '175.45.221.223',
        'api_source': {
            'accessKey': 'mYUP1ZqESUOpjyOokWC8',
            'secretKey': '31scunD8FAtSTqU92X2DYFsi1UaiEbQ5qrTxi2aM',
            'ncloudUrl': 'https://ncloud.apigw.gov-ntruss.com',
            'billingApiUrl': 'https://billingapi.apigw.gov-ntruss.com'
        },
        'dbSource': {
            'dbName': 'cdm_fix',
            'schemaName': 'test',
            'host': '175.45.221.223',
            'port': '26257',
            'user': 'root'
        }
    }
    src_client = ApiClient(config1)
    tgt_client = ApiClient(config2)
