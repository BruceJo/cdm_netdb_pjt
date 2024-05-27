import time
import sys
import getConfig as gcf
# pip install pickle-mixin
import pickle
from datetime import datetime,timezone
from dateutil.relativedelta import relativedelta
import hmac
import hashlib
import base64
import json
import requests
import re
import subprocess

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
    
    def make_pre_result(self):
        _from, _to = self.trans_utc(self.period_time, self.period_unit)
        now_res = self.cc.send_request(_from, _to)
        
        with open(binary_path, 'wb') as file: 
            pickle.dump(now_res, file)
        
    def run(self):
        _from, _to = self.trans_utc(self.period_time, self.period_unit)
        now_res = self.cc.send_request(_from, _to)
        
        try:
            with open(binary_path, 'rb') as file: 
                pre_res = pickle.load(file)
        except FileNotFoundError:
            write_status('init')
            return False

        diff_cnt = len(set(now_res) - set(pre_res))

        if diff_cnt:
            print(set(now_res), type(now_res))
            print(set(pre_res), type(pre_res))
            print('diff_cnt : ', diff_cnt)
            # 10 : pushDeltaInfo(Async) -> RMQ로 비동기 전달
            # ★ diff_json -> sub process parameter ★
            subprocess.Popen([sys.executable or 'python', 'cyclicSub.py', status_path, config_path, binary_path, ])

            with open(binary_path, 'wb') as file: 
                pickle.dump(now_res, file)


def check_status(stat):
    # stat : init, idle, run
    try:
        with open(status_path, 'r') as sts:
            last_line = sts.readlines()[-1]
        return True if last_line == stat else False
    except:
        return False

def write_status(stat):
    # stat : init, idle, run
    with open(status_path, 'w') as sts:
        sts.write(stat)

def read_conf():   
    return gcf.Config(config_path).getConfig()


if __name__ == '__main__':
    status_path = sys.argv[1]
    config_path = sys.argv[2]
    # for test
    # status_path = "../conf/status.conf"
    # config_path = "../conf/app.conf"
    binary_path = "./history.pkl"
    
    
    while True:
        gh = History(read_conf()['API-SOURCE-NAVER-CLOUD'], read_conf()['CYCLIC-SYNC'])
        every = int(gh.to_sec(gh.every_time, gh.every_unit))
        print("subprocess loop start")

        if check_status('init'):
            gh.make_pre_result()
            write_status('idle')

        else:   # idle or run
            gh.run()
            ## get activity_log
            ## set now_result
            ## cal diff_result
            ## if diff_result == True :
                # push delta to NS (async)
                ## write_status('run')
                ## start_time = str(int(time.time() * 1000))
                ## resource_schema_name = "rs_" + start_time
                ## create schema
                ## get resource_info_from_api
                ## try: insert info
                ## get last_schema = schemaNames.find('rs_').split('rs_')[0].max()
                
                ## if last_schema < start_time: set schema (request to main)
                    ## set pre_result @main request
                    # get resouece_info_from_db
                    # push resource_info_from_db
                
                ## get schema_list
                # if len(schema_list) >= schema_retention_policy: drop old schemas
                ## write_status('idle')
        print("subprocess loop end")
        time.sleep(every)