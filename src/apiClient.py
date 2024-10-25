import requests
import json


class ApiClient:
    def __init__(self, config):
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

    def set_resource_info(self):
        data = {
            "dbName": self.database["dbName"],
            "schemaName": self.database["schemaName"],
            "host": self.database["host"],
            "port": self.database["port"],
            "user": self.database["user"]
        }
        payload = json.dumps(data)
        response = requests.post(f"{self.base_url}/set_resource_info", data=payload, headers=self.headers)
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
    # src
    config1 = {
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
    # tgt
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
            'schemaName': 'lhb_test_0526_1',
            'host': '175.45.214.45',
            'port': '26257',
            'user': 'root'
        }
    }
    src_client = ApiClient(config1)
    tgt_client = ApiClient(config2)
    print(src_client.create_schema())
    print(src_client.read2insert())
    print(src_client.create_recovery())
    # print(src_client.set_resource_info())
    # result = src_client.create_schema()
    # print(result)
    # result = tgt_client.create_schema()
    # print(result)
