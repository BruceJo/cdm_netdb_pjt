import json
import requests
import hmac
import hashlib
import base64
import time
import re
from datetime import datetime,timezone
from dateutil.relativedelta import relativedelta
import getConfig as gcf
# pip install pickle-mixin
import pickle
import os
import naverCloud
import psycopg2
import connDbnApi as cda
import getConfig as gcf
def GetSchemaList(destination):
    try:
        conn = cda.Connect(db = destination).connect_cockroachdb()
        cursor = conn.cursor()
        query = """
            SELECT table_name, column_name 
            FROM information_schema.columns 
            WHERE table_schema = 'public';
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        schema = {}
        for row in rows:
            table_name = row[0]
            column_name = row[1]
            if table_name not in schema:
                schema[table_name] = []
            schema[table_name].append(column_name)
        
        return schema
        
    except psycopg2.Error as e:
        print("PostgreSQL 오류 발생:", e)
        return None
        
    finally:
        if conn:
            conn.close()

source = app_conf['DATABASE-SOURCE'].copy()      
schema = GetSchemaList()
if schema:
    print("데이터베이스 스키마:")
    for table, columns in schema.items():
        print(f"테이블 '{table}': {columns}")
else:
    print("스키마를 가져올 수 없습니다.")

def SetStartTimestamp():
    return datetime.now()

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
    
    def send_request(self, _from, _to):
        timestamp = str(int(time.time() * 1000))
        signature = self.create_signature(timestamp)
        
        
        http_header = {
            'Content-Type': 'application/json; charset=utf-8',
            'x-ncp-apigw-timestamp': timestamp,
            'x-ncp-iam-access-key': self.access_key,
            'x-ncp-apigw-signature-v2': signature
        }
        print('http_header', http_header)
        
        # https://api-gov.ncloud-docs.com/docs/management-cloudactivitytracer-getactivitylist
        json_body = {
            "fromEventTime": str(_from),
            "toEventTime": str(_to),
            # "nrn": "string",
            # "pageIndex": "int",
            "pageSize": "20"
        }
        
        res_dict = {}
        idx = 0
        while True:
            json_body.update({"pageIndex" : str(idx)})
            response = requests.post(self.http_url + self.api_url, 
                                     data=json.dumps(json_body), 
                                     headers=http_header)
            sub_res = json.loads(response.text)
            idx += 1

            if sub_res['itemCount'] != 0:
                # res_dict.update({x['historyId']: x for x in sub_res})
                res_dict.update({x['historyId']: x for x in sub_res['items'] if x['actionDisplayName']!='Login'})
            else:
                break
            
        return res_dict
    

class History():
    def __init__(self, target_api, gcch_durat):
        self.target_api = target_api
        self.every_time, self.every_unit = self.split_duration(gcch_durat['every'])
        self.period_time, self.period_unit = self.split_duration(gcch_durat['period'])
        self.cc = Tracer(api=target_api)
    
    def split_duration(self, durat):
        return float(re.findall('(\d+(?:\.\d+)?)', durat)[0]), re.findall('[a-zA-Z]+', durat)[0]

    def trans_utc(self, num, unit):
        match_dict = {'y' : 'years', 'M' : 'months', 'w' : 'weeks', 'd' : 'days', 'h' : 'hours',  
                      'm' : 'minutes', 's' : 'seconds', 'ms' : 'microseconds'}
        to_time = datetime.now(timezone.utc)
        kwarg = {match_dict[unit] : num} if unit != 'ms' else {match_dict[unit] : num*1000}
        from_time = to_time - relativedelta(**kwarg)
        
        to_utc = int(to_time.timestamp() * 1000)
        from_utc = int(from_time.timestamp() * 1000)
        
        return from_utc, to_utc

    def to_sec(self, num, unit):
        from_utc, to_utc = self.trans_utc(num, unit)
        return (to_utc - from_utc) / 1e3
    
    def trigger_to_ns(self):
        body = {}

        # 비동기처럼 응답을 기다리지 않고 post
        try:
            requests.post("http://localhost:9999/some_url", 
                          data=json.dumps({'Tagkey':body}), 
                          headers={'Content-Type': 'application/json'}, 
                          timeout=0.0000000001)
        except requests.exceptions.ReadTimeout: 
            pass

        ...

    def run(self):
        _from, _to = self.trans_utc(self.period_time, self.period_unit)
        now_res = self.cc.send_request(_from, _to)
        
        if not os.path.isfile(DICT_PATH):
            pre_res = {}
        else:
            with open(DICT_PATH, 'rb') as file: 
                pre_res = pickle.load(file)
        
        print(set(now_res), type(now_res))
        print(set(pre_res), type(pre_res))
        diff_cnt = len(set(now_res) - set(pre_res))

        print('diff_cnt : ', diff_cnt)
        
        if diff_cnt:
            ...

        with open(DICT_PATH, 'wb') as file: 
            pickle.dump(now_res, file)

if __name__ == '__main__':
    DICT_PATH = "./history.pkl"
    CONF_PATH = "C:/Users/yubin/OneDrive/바탕 화면/대외활동/NETDB/cdm/cdm_netdb_pft_yuvnn/conf"
    
    app_conf = gcf.Config(CONF_PATH).getConfig()

    api_target = app_conf['API-TARGET-NAVER-CLOUD'].copy()
    gcch_durat = app_conf['GET-CLOUD-CHANGE-HISTORY'].copy()

    gh = History(api_target, gcch_durat)
    repeat_time = gh.to_sec(gh.every_time, gh.every_unit)
    print('repeat_time', repeat_time)
    gh.run()
