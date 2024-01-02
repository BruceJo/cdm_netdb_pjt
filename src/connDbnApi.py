import hmac
import hashlib
import base64
import psycopg2
import requests
import time
import urllib
import json

class Connect():
    def __init__(self, api=None, db=None):
        if api != None:
            self.secret_key = api['secretKey']
            self.access_key = api['accessKey']
            self.ncloudUrl = api['ncloudUrl']
            self.billingApiUrl = api['billingApiUrl']
        if db != None:
            self.db_name = db['dbName']
            self.host = db['host']
            self.port = db['port']
            self.user = db['user']

    # conn api
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
        response = requests.get(self.ncloudUrl + api_url, headers=http_header)
        result = json.loads(response.text)
        if 'error' in result.keys() and result['error']['errorCode'] == '300':
            response = requests.get(self.billingApiUrl + api_url, headers=http_header)
            result = json.loads(response.text)

        return result

    def request_api(self, api_url, sub_url, **params):
        timestamp = str(int(time.time() * 1000))
        method = "GET"
        api_url = (f"/{api_url}/{sub_url}"
                "?regionCode=KR"
                "&responseFormatType=json")
        check_bool = lambda x: str(x).lower() if isinstance(x, bool) else str(x)
        param_format = "".join([f"&{k}={urllib.parse.quote(check_bool(v))}" for k, v in params.items()])

        response = self.send_request(method, api_url+param_format, timestamp)

        return response
    
    ## conn db
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