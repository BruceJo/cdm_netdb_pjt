from flask import Flask, request
from flask_cors import CORS
import getConfig as gcf
import createSchema as cs
import readVPC2InsertDB as rv2
import createVPC
import vudVPC
import getHistory as gh
import subprocess
from subprocess import PIPE
import configparser as parser


#Flask init
app = Flask(__name__)
CORS(app)

# function
def change_default(req, obj, req_key):
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
    #     "schemaName" : "{your_}",
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
    
    cock_create = cs.Create(source) 
    cock_create.create_schema() 
    cock_create.create_table()
    return 'success'


@app.route('/read2insert', methods=['POST'])
def read2insert(): # naver cloud 에서 source를 가지고옴 
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
    
    dv = vudVPC.VUD(api_target, req['delete'], 'd')
    
    return dv.run()


# Server Run
if __name__ == '__main__':
    # CONF_PATH = "./conf/app.conf"
    # app_conf = gcf.Config(CONF_PATH).getConfig() 

    
    interpreter = "C://Users//yubin//AppData//Local//Programs//Python//Python312//python.exe"
    process = subprocess.Popen([interpreter,'getHistory.py'], shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process_id = process.pid 
    
    # StartTime = gh.SetStartTimestamp()
    # print(StartTime)

 
    # SCHEMARETENTIONPOLICY=5
    
    # RunStatus=False
    # cv3 = createVPC.Create(db_source, api_target)
    # getDB = cv3.get_table()
    # NowResult = ''
    # PreResult = ''

    # #  초기화
    # if RunStatus == False:
    #     print("44")
    #     print("systemError : not found subprocess")
    #     if not getDB:
    #         create_db()
    #     app_conf['schemaName'] = {StartTime}
    #     insert_error = read2insert()
    #     if insert_error != 'success':
    #         app_conf['schemaName'] = {StartTime}
    #         initFlag = True
    #         pid = sub_proc.pid

    # # 처음 실행
    # if initFlag == True:
    #     PreResult = gh.History.get_ActivityLog()
    #     initFlag = False

    # # 처음 실행이 아님 => 최신화 시작
    # while(not initFlag):
    #     diff = gh.History.run()
    #     if (diff):
    #         gh.SetRunStatus()
    #         StartTime = gh.SetStartTimestamp()
    #         gh.GetResourceinfo(app_conf)
    #         app_conf['schemaName'] = {StartTime}
    #         cs.create_schema()
    #         insert_error = read2insert()

    #         schemaName = gh.SchemManager.GetResourceinfo(app_conf) #정렬되어 있으니까 하나만 가져와서 비교

    #         if (insert_error != 'success' and schemaName < StartTime):
    #             app_conf['schemaName'] = {StartTime}
    #             PreResult = gh.History.get_ActivityLog()
    #             getResource = gh.SchemManager.GetResourceinfo(app_conf)
    #             gh.trigger_to_ns(getResource)
    #     schemaList = gh.SchemManager.GetSchemaList(app_conf)
    #     if len(schemaList) >= SCHEMARETENTIONPOLICY:
    #         gh.SchemManager.DropSchema(app_conf)

    #     app.run(threaded=True, debug=True, host='0.0.0.0', port=9999)