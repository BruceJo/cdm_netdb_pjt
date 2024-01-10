from flask import Flask, request
from flask_cors import CORS
import getConfig as gcf #getConfig라는 모듈을 gcf라는 이름으로 import
import createSchema
import readVPC2InsertDB as rv2
import createVPC
import vudVPC

#Flask init
app = Flask(__name__)
CORS(app)

# function
def change_default(req, obj, req_key): #그러니깐 req 딕셔너리의 key중에 req_key가 존재한다면 req_key에 해당하는 item()을 꺼내서 obj딕셔너리에 복사해주는 느낌임
    if req_key in req.keys():
        for k, v in req[req_key].items():
            obj[k] = v
    return obj

# route
@app.route('/create_schema', methods=['POST'])
def create_db():
    # request format. Required ["dbSource"]["schemaName"]
    # {
    #     "dbName" : "cdm_fix",
    #     "schemaName" : "{your_schema_name}",
    #     "host" : "223.130.173.142",
    #     "port" : "26257",
    #     "user" : "root"
    # }
    req = request.get_json()
    if 'schemaName' not in req:
        return 'fail, need key ["schemaName"]', 400
    
    source = app_conf['DATABASE-SOURCE'].copy()
    
    for k, v in req.items():
        source[k] = v
    
    cock_create = createSchema.Create(source) #createSchema.Create 클래스의 인스턴스를 생성합니다.
    cock_create.create_schema()
    cock_create.create_table()
    cock_create.create_sequence() #240102 cdh
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
    #         "host": "223.130.173.142",
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
    
    api = change_default(req, api, 'apiSource') # 이 작업이 필요한 이유는 요청을 보낼때 기본값과 변경된 값이 있다면 원래 값과 변경된 값의 병합을 위해서 필요함
    source = change_default(req, source, 'dbSource') #위와 이유 같음
    
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
    #         "host": "223.130.173.142",
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
# <<<<<<< HEAD
    print(req)
   # if 'dbSource' not in req:
# =======
    if 'dbSource' not in req:
# >>>>>>> b9b348e066201175cf803f1156ed890c16d40600
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
    # request format. Required ["view"]["target"]
    # {
    #     "apiTarget": {
    #         "accessKey": "mYUP1ZqESUOpjyOokWC8",
    #         "secretKey": "31scunD8FAtSTqU92X2DYFsi1UaiEbQ5qrTxi2aM",
    #         "ncloudUrl": "https://ncloud.apigw.gov-ntruss.com",
    #         "billingApiUrl": "https://billingapi.apigw.gov-ntruss.com"
    #     },
    #     "read" : {
    #         "target" : "RouteTable"
    #     }
    # }
    req = request.get_json()
    if 'read' not in req: 
        return 'fail, need key ["read"]', 400
    elif 'target' not in req['read']:
        return 'fail, need key ["read"]["target"]', 400
    
    api_target = app_conf['API-TARGET-NAVER-CLOUD'].copy()
    api_target = change_default(req, api_target, 'apiTarget')
    
    vv = vudVPC.VUD(api_target, req['read'], 'r')
    
    return vv.run()


@app.route('/update_vpc', methods=['POST'])
def update_vpc():
    # request format. Required ["update"]["target"], ["update"]["body"]
    # {
    #     "apiTarget": {
    #         "accessKey": "mYUP1ZqESUOpjyOokWC8",
    #         "secretKey": "31scunD8FAtSTqU92X2DYFsi1UaiEbQ5qrTxi2aM",
    #         "ncloudUrl": "https://ncloud.apigw.gov-ntruss.com",
    #         "billingApiUrl": "https://billingapi.apigw.gov-ntruss.com"
    #     },
    #     "update" : {
    #         "target" : "RouteTable",
    #         "key" : "{some_your_key}", //If there are two or more update APIs, specify the API address
    #         "body" : {
    #             "routeTableNo" : "20247",
    #             "routeTableDescription" : "many thanks, Jo."
    #         }
    #     }
    # }
    req = request.get_json()
    if 'update' not in req:
        return 'fail, need key ["update"]', 400
    elif 'target' not in req['update']:
        return 'fail, need key ["update"]["target"]', 400
    elif 'body' not in req['update']:
        return 'fail, need key ["update"]["body"]', 400

    api_target = app_conf['API-TARGET-NAVER-CLOUD'].copy()
    api_target = change_default(req, api_target, 'apiTarget')
    
    uv = vudVPC.VUD(api_target, req['update'], 'u')
    
    return uv.run()


@app.route('/delete_vpc', methods=['POST'])
def delete_vpc():
    # request format. Required ["delete"]["target"], ["delete"]["body"]
    # {
    #     "apiTarget": {
    #         "accessKey": "mYUP1ZqESUOpjyOokWC8",
    #         "secretKey": "31scunD8FAtSTqU92X2DYFsi1UaiEbQ5qrTxi2aM",
    #         "ncloudUrl": "https://ncloud.apigw.gov-ntruss.com",
    #         "billingApiUrl": "https://billingapi.apigw.gov-ntruss.com"
    #     },
    #     "delete" : {
    #         "target" : "RouteTable",
    #         "key" : "{some_your_key}", //If there are two or more delete APIs, specify the API address
    #         "body" : {
    #             "routeTableNo" : "20247"
    #         }
    #     }
    # }
    req = request.get_json()
    if 'delete' not in req: 
        return 'fail, need key ["delete"]', 400
    elif 'target' not in req['delete']:
        return 'fail, need key ["delete"]["target"]', 400
    elif 'body' not in req['delete']:
        return 'fail, need key ["delete"]["body"]', 400

    api_target = app_conf['API-TARGET-NAVER-CLOUD'].copy()
    api_target = change_default(req, api_target, 'apiTarget')
    
    ud = vudVPC.VUD(api_target, req['delete'], 'd')
    
    return ud.run()


# Server Run
if __name__ == '__main__':
    CONF_PATH = "../conf/app.conf"
    app_conf = gcf.Config(CONF_PATH).getConfig()
    
    app.run(threaded=True, debug=True, host='0.0.0.0', port=9999)