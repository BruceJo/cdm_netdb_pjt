import connDbnApi as cda
import naverCloud
import json

class View():
    def __init__(self, api_target, req_target):
        self.api_target = api_target
        self.req_target = req_target
        self.cc = cda.Connect(api=api_target)
    
    def set_url(self, name, action):
        self.table_name, self.api_url, self.sub_url = naverCloud.set_url(name, action)

    def view(self):
        self.set_url(self.req_target['name'], 'read')
        res = self.cc.request_api(self.api_url, self.sub_url)
        return json.dumps(res)