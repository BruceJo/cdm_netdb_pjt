from flask import Flask, request
from flask_cors import CORS
import getConfig as gcf
import createSchema
import readVPC2InsertDB as rv2
import viewVPC
import createVPC
import updateVPC

#Flask init
app = Flask(__name__)
CORS(app)

def change_default(req, obj, req_key):
    if req_key in req.keys():
        for k, v in req[req_key].items():
            obj[k] = v
    return obj

@app.route('/create_schema', methods=['POST'])
def create_db():
    # request format. Required ["dbSource"]["schemaName"]
    # {
    #     "dbName" : "cdm_fix",
    #     "schemaName" : "{your_schema_name}",
    #     "host" : "211.188.69.4",
    #     "port" : "26257",
    #     "user" : "root"
    # }
    req = request.get_json()
    if 'schemaName' not in req: 
        return 'fail, need key ["schemaName"]', 400
    
    source = app_conf['DATABASE-SOURCE'].copy()
    
    for k, v in req.items():
        source[k] = v
    
    cock_create = createSchema.Create(source)
    cock_create.create_schema()
    cock_create.create_table()

    return 'success'

@app.route('/read2insert', methods=['POST'])
def read2insert():
    # request format. Required ["dbSource"]["schemaName"]
    # {
    #     "apiSource": {
    #         "accessKey": "mYUP1ZqESUOpjyOokWC8",
    #         "secretKey": "31scunD8FAtSTqU92X2DYFsi1UaiEbQ5qrTxi2aM",
    #         "ncloudUrl": "https://ncloud.apigw.gov-ntruss.com",
    #         "billingApiUrl": "https://billingapi.apigw.gov-ntruss.com"
    #     },
    #     "dbSource": {
    #         "dbName": "cdm_fix",
    #         "schemaName": "{your_schema_name}",
    #         "schemaPath": "../schema/naverCloudSchema.sql",
    #         "host": "211.188.69.4",
    #         "port": "26257",
    #         "user": "root"
    #     }
    # }
    req = request.get_json()
    if 'dbSource' not in req: 
        return 'fail, need key ["dbSource"]', 400
    elif 'schemaName' not in req['dbSource']:
        return 'fail, need key ["dbSource"]["schemaName"]', 400
    
    api = app_conf['API-SOURCE-NAVER-CLOUD'].copy()
    source = app_conf['DATABASE-SOURCE'].copy()
    
    api = change_default(req, api, 'apiSource')
    source = change_default(req, source, 'dbSource')
    
    ri = rv2.Read2Insert(api, source)
    ri.run()

    return 'success'


@app.route('/create_vpc', methods=['POST'])
def create_vpc():
    # request format. Required ["dbSource"]["schemaName"]
    # {
    #     "dbSource": {
    #         "dbName": "cdm_fix",
    #         "schemaName": "{your_schema_name}",
    #         "host": "211.188.69.4",
    #         "port": "26257",
    #         "user": "root"
    #     },
    #     "apiTarget": {
    #         "accessKey": "mYUP1ZqESUOpjyOokWC8",
    #         "secretKey": "31scunD8FAtSTqU92X2DYFsi1UaiEbQ5qrTxi2aM",
    #         "ncloudUrl": "https://ncloud.apigw.gov-ntruss.com",
    #         "billingApiUrl": "https://billingapi.apigw.gov-ntruss.com"
    #     }
    # }
    req = request.get_json()
    if 'dbSource' not in req: 
        return 'fail, need key ["dbSource"]', 400
    elif 'schemaName' not in req['dbSource']:
        return 'fail, need key ["dbSource"]["schemaName"]', 400
    
    db_source = app_conf['DATABASE-SOURCE'].copy()
    api_target = app_conf['API-TARGET-NAVER-CLOUD'].copy()

    db_source = change_default(req, db_source, 'dbSource')
    api_target = change_default(req, api_target, 'apiTarget')
    
    # print(db_source, '\n', api_target)
    cv = createVPC.Create(db_source, api_target)
    cv.run()

    return 'success'

@app.route('/view_vpc', methods=['POST'])
def view_vpc():
    # request format. Required ["target"]["name"]
    # {
    #     "apiTarget": {
    #         "accessKey": "mYUP1ZqESUOpjyOokWC8",
    #         "secretKey": "31scunD8FAtSTqU92X2DYFsi1UaiEbQ5qrTxi2aM",
    #         "ncloudUrl": "https://ncloud.apigw.gov-ntruss.com",
    #         "billingApiUrl": "https://billingapi.apigw.gov-ntruss.com"
    #     },
    #     "target" : {
    #         "name" : "RouteTable"
    #     }
    # }
    req = request.get_json()
    if 'target' not in req: 
        return 'fail, need key ["target"]', 400
    elif 'name' not in req['target']:
        return 'fail, need key ["target"]["name"]', 400
    
    api_target = app_conf['API-TARGET-NAVER-CLOUD'].copy()
    api_target = change_default(req, api_target, 'apiTarget')
    
    vv = viewVPC.View(api_target, req['target'])
    
    return vv.view()


# @app.route('/update_vpc', methods=['POST'])
# def update_vpc():
#     req = request.get_json()
#     if 'action' not in req: 
#         return 'fail, need key ["action"]', 400
#     elif req['action'] not in ['check', 'update']:
#         return 'fail, need value ["action"] : { "check" | "update" }', 400

#     api_target = app_conf['API-TARGET-NAVER-CLOUD'].copy()
#     api_target = change_default(req, api_target, 'apiTarget')
    
#     if req['action'] == 'check':
#         return updateVPC.Update(api_target).check()
#     elif req['action'] == 'update':
#         if 'update' not in req:
#             return 'fail, need update details', 400
#         return 'success'


#Server Run
if __name__ == '__main__':
    CONF_PATH = "../conf/app.conf"
    app_conf = gcf.Config(CONF_PATH).getConfig()
    
    app.run(threaded=True, debug=True, host='0.0.0.0', port=9999)