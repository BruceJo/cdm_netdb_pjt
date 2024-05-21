import datetime
import subprocess
import sys
import atexit
from flask import Flask, request
from flask_cors import CORS
import getConfig as gcf
import createSchema
import readVPC2InsertDB as rv2
import createVPC
import vudVPC
import connDbnApi as cda
# import createALL

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
def create_schema():
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
    
    source = read_conf()['DATABASE-INFO'].copy()
    
    for k, v in req.items():
        source[k] = v
    
    cock_create = createSchema.Create(source)
    cock_create.create_schema()
    cock_create.create_table()
    return 'success'

@app.route('/create_recovery', methods=['POST'])
def create_recovery():
    # request format
    # {}, empty json
    source = read_conf()['DATABASE-INFO'].copy()
    
    for k, v in source.items():
        if k == 'schemaName':
            source[k] = 'recovery'
        elif k == 'schemaPath':
            source[k] = source['recoverySchemaPath']
        else:
            source[k] = v

    print(source)
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
    
    api = read_conf()['API-SOURCE-NAVER-CLOUD'].copy()
    source = read_conf()['DATABASE-INFO'].copy()
    
    api = change_default(req, api, 'apiSource')
    source = change_default(req, source, 'dbSource')
    
    ri = rv2.Read2Insert(api, source)
    ri.run()

    return 'success'

def is_subproc_run():
    try:
        with open(status_path, 'r') as sts:
            last_line = sts.readlines()[-1]
        return True if last_line == 'run' else False

    except:
        with open(status_path, 'w') as sts:
            sts.write("init")
        return False

def existence_db(db_source):
    constant_db_name = db_source['dbName']
    db_source['dbName'] = None
    cd = cda.Connect(db=db_source)
    db_source['dbName'] = constant_db_name
    
    if not constant_db_name in [x['database_name'] for x in cd.check_db()]:
        cd.create_db(constant_db_name)
        print("Created, db list : ", [x['database_name'] for x in cd.check_db()])
    else:
        print("Already exists, db list : ", [x['database_name'] for x in cd.check_db()])

def create_resource_schema(source, rsn):
    source['schemaName'] = rsn
    cock_create = createSchema.Create(source)
    cock_create.create_schema()
    cock_create.create_table()

def read_conf():   
    return gcf.Config(config_path).getConfig()

@app.route('/sync_cluster', methods=['POST'])
def sync_cluster():
    global RESOURCE_SCHEMA
    start_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    resource_schema_name = "RS_"+start_time

    if is_subproc_run():
        return {"warning" : "Work already in progress."}
    else:
        db_source = read_conf()['DATABASE-INFO'].copy()
        existence_db(db_source)
        create_resource_schema(db_source, resource_schema_name)
        db_source['schemaName'] = resource_schema_name
        print(db_source)

        api = read_conf()['API-SOURCE-NAVER-CLOUD'].copy()
        ri = rv2.Read2Insert(api, db_source)
        try:
            ri.run()
        except:
            return {"error" : "insert error."}
        
        RESOURCE_SCHEMA = resource_schema_name
        # update config file
        # https://stackoverflow.com/questions/8884188/how-to-read-and-write-ini-file-with-python3

        # wakeup subprocess
        # status_path : init -> idle

        # return Sync result (ri attribute)
        return 'a'


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
    
    db_source = read_conf()['DATABASE-INFO'].copy()
    api_target = read_conf()['API-TARGET-NAVER-CLOUD'].copy()

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
    
    api_target = read_conf()['API-TARGET-NAVER-CLOUD'].copy()
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

    api_target = read_conf()['API-TARGET-NAVER-CLOUD'].copy()
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

    api_target = read_conf()['API-TARGET-NAVER-CLOUD'].copy()
    api_target = change_default(req, api_target, 'apiTarget')
    
    ud = vudVPC.VUD(api_target, req['delete'], 'd')
    
    return ud.run()


# Server Run
if __name__ == '__main__':
    status_path = "../conf/status.conf"
    config_path = "../conf/app.conf"
    RESOURCE_SCHEMA = read_conf()['DATABASE-INFO']['schemaName']
    print('origin :', RESOURCE_SCHEMA)

    if 1:
        cyclic_sync = subprocess.Popen([sys.executable or 'python', 'test.py'])    #For Test
        atexit.register(cyclic_sync.kill)
    
    app.run(threaded=True, debug=True, host='0.0.0.0', port=9999)