import hmac
import hashlib
import base64
import psycopg2
import requests
import time

class Connect():
    def __init__(self, api=None, destination=None):
        if api != None:
            self.secret_key = api['secretKey']
            self.access_key = api['accessKey']
            self.base_url = api['baseUrl']
        if destination != None:
            self.db_name = destination['dbName']
            self.host = destination['host']
            self.port = destination['port']
            self.user = destination['user']

    def create_signature(self, method, api_url, timestamp):
        secret_key_bytes = bytes(self.secret_key, 'UTF-8')
        message = bytes(f"{method} {api_url}\n{timestamp}\n{self.access_key}", 'UTF-8')
        signing_key = base64.b64encode(hmac.new(secret_key_bytes, message, digestmod=hashlib.sha256).digest())
        return signing_key
    
    def send_request(self, method, api_url, timestamp):
        signature = self.create_signature(method, api_url, timestamp)
        http_header = {
            'x-ncp-apigw-timestamp': timestamp,
            'x-ncp-iam-access-key': self.access_key,
            'x-ncp-apigw-signature-v2': signature
        }
        full_url = self.base_url + api_url
        response = requests.get(full_url, headers=http_header)
        return response

    def connect_cockroachdb(self):
        try:
            connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.db_name,
                user=self.user,
            )
            return connection
        except Exception as e:
            print(f"Database connection failure: {e}")
            return None

    def get_list(self, api_url, sub_url):
        timestamp = str(int(time.time() * 1000))
        method = "GET"
        api_url = (f"/{api_url}/{sub_url}"
                   "?regionCode=KR"
                   "&responseFormatType=json"
        )
        print('api_url', api_url)
        response = self.send_request(method, api_url, timestamp)
        
        return response.text

    def get_route_list(self, api_url, sub_url, vpc_no, route_table_no):
        timestamp = str(int(time.time() * 1000))
        method = "GET"
        api_url = (f"/{api_url}/v2/{sub_url}"
                "?regionCode=KR"
                "&responseFormatType=json" # json으로 받아오기
                f"&vpcNo={vpc_no}"
                f"&routeTableNo={route_table_no}"
            # "&vpcStatusCode=RUN"
                )
        response = self.send_request(method, api_url, timestamp)
        
        return response.text

    def query_db(self, q):
        conn = self.connect_cockroachdb()
        cur = conn.cursor()

        cur.execute(f"use {self.db_name};")
        cur.execute(q)
        rows = cur.fetchall()
        cols = [column[0] for column in cur.description]
        
        response = []
        for row in rows:
            response.append(dict(zip(cols, row)))
        
        cur.close()
        conn.close()

        return response