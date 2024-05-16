import naverCloud
import connDbnApi as cda
import json

class VUD():    # view, update, delete
    def __init__(self, api_target, req_target, flag):
        self.api_target = api_target
        self.req_target = req_target
        self.cc = cda.Connect(api=api_target)
        self.flag = flag
    
    def set_url(self, name, action, *choice):
        self.table_name, self.api_url, self.sub_url = naverCloud.set_url(name, action, *choice)

    def run(self):
        try:
            if 'key' in self.req_target:
                self.set_url(self.req_target['target'], self.flag, self.req_target['key'])
            else:
                self.set_url(self.req_target['target'], self.flag)
        except KeyError as e:
            return f"[ERR] Not found your "+str(e), 400
        except NameError as e:
            return f"[ERR] Required field is not specified. location : ['key'], value : "+str(e), 400
        
        if self.flag == 'r':
            res = self.cc.request_api(self.api_url, self.sub_url)
            return json.dumps(res)
        else:
            res = self.cc.request_api(self.api_url, self.sub_url, **self.req_target['body'])
            return json.dumps(res)