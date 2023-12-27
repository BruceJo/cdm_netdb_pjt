from flask import Flask, request, Response
from flask_cors import CORS
import json
# import requests
import getConfig as gcf
import createDB
import readVPC2InsertDB as rv2
import createVPC

#Flask init
app = Flask(__name__)
CORS(app)

@app.route('/create_db', methods=['POST'])
def create_db():
    # request format
    # {
    #     "dbName" : "cdm_fix",
    #     "schemaName" : "{your_schema_name}",
    #     "host" : "211.188.69.4",
    #     "port" : "26257",
    #     "user" : "root"
    # }
    req = request.get_json()
    source = app_conf['SOURCE-NAVER-CLOUD'].copy()
    
    for k, v in req.items():
        source[k] = v
    
    cock_create = createDB.Create(source)
    cock_create.create_schema()
    cock_create.create_table()

    return 'sucess'

@app.route('/read2insert', methods=['POST'])
def read2insert():
    # {
    #     "api": {
    #         "accessKey": "mYUP1ZqESUOpjyOokWC8",
    #         "secretKey": "31scunD8FAtSTqU92X2DYFsi1UaiEbQ5qrTxi2aM",
    #         "ncloudUrl": "https://ncloud.apigw.gov-ntruss.com",
    #         "billingApiUrl": "https://billingapi.apigw.gov-ntruss.com"
    #     },
    #     "source": {
    #         "dbName": "cdm_fix",
    #         "schemaName": "test_schema",
    #         "schemaPath": "../schema/naverCloudSchema.sql",
    #         "host": "211.188.69.4",
    #         "port": "26257",
    #         "user": "root"
    #     }
    # }
    req = request.get_json()
    api = app_conf['API'].copy()
    source = app_conf['SOURCE-NAVER-CLOUD'].copy()
    
    # print({'api' : api, 'source' : source})

    def change_default(obj, req_key):
        if req_key in req.keys():
            for k, v in req[req_key].items():
                obj[k] = v
    change_default(api, 'api')
    change_default(source, 'source')
    
    ri = rv2.Read2Insert(api, source)
    ri.run()

    return 'sucess'


@app.route('/create_vpc', methods=['POST'])
def create_vpc():
    #req = request.get_json()
    api = app_conf['API']
    source = app_conf['SOURCE-NAVER-CLOUD']
    target = app_conf['TARGET-NAVER-CLOUD']

    # for k, v in req.items():
    #     source[k] = v
    
    cv = createVPC.Create(api, source, target)
    cv.run()

    return 'sucess'

#Server Run
if __name__ == '__main__':
    CONF_PATH = "../conf/app.conf"
    app_conf = gcf.Config(CONF_PATH).getConfig()
    
    app.run(threaded=True, debug=True, host='0.0.0.0', port=9999)