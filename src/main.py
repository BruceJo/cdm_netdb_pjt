import time
import subprocess
import sys
import os
import atexit
import pickle
import json
import requests
from flask import Flask, request
from flask_cors import CORS
import pandas as pd
# pip install sqlalchemy-cockroachdb
from sqlalchemy import create_engine
import getConfig as gcf
import createSchema
import readVPC2InsertDB as rv2
import createVPC
import vudVPC
import connDbnApi as cda

#Flask init
app = Flask(__name__)
CORS(app)

# function
def change_default(req, obj, req_key):
    if req_key in req.keys():
        for k, v in req[req_key].items():
            obj[k] = v
    return obj

def is_subproc_run(stat):
    # stat : init, idle, run
    try:
        with open(status_path, 'r') as sts:
            last_line = sts.readlines()[-1]
        return True if last_line == stat else False
    except:
        return False

def set_subproc_status():
    if os.path.isfile(status_path):
        with open(status_path, 'r') as sts:
            last_line = sts.readlines()[-1]
        if last_line not in ['init', 'idle', 'run']:
            with open(status_path, 'w') as sts:
                sts.write("init")
    else:
        with open(status_path, 'w') as sts:
                sts.write("init")

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

def create_resource_schema(source, schema_name):
    source['schemaName'] = schema_name
    cock_create = createSchema.Create(source)
    cock_create.create_schema()
    cock_create.create_table()

def read_conf():
    return gcf.Config(config_path).getConfig()

def insert_to_detail_engine(db_info):
    connection_string = f"cockroachdb://{db_info['user']}@{db_info['host']}:{db_info['port']}/{db_info['dbName']}"
    print(connection_string)
    engine = create_engine(connection_string)
    return engine

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

@app.route('/sync_cluster', methods=['POST'])
def sync_cluster():
    global RESOURCE_SCHEMA
    start_time = str(int(time.time() * 1000))
    resource_schema_name = "rs_" + start_time

    if is_subproc_run('run'):
        return {"warning" : "Work already in progress."}, 200
    else:
        db_source = read_conf()['DATABASE-INFO'].copy()
        existence_db(db_source)
        create_resource_schema(db_source, resource_schema_name)
        db_source['schemaName'] = resource_schema_name

        api = read_conf()['API-SOURCE-NAVER-CLOUD'].copy()
        ri = rv2.Read2Insert(api, db_source)
        try:
            ri.run()
        except:
            return {"error" : "insert error."}, 500
        
        RESOURCE_SCHEMA = resource_schema_name
        # update config file
        gcf.Config(config_path).updateConfig('DATABASE-INFO', 'schemaName', resource_schema_name)

        # wakeup subprocess = if not exist status then status_path : N/A -> init
        set_subproc_status()

        # return Sync result (if you want attribute then get form db)
        return {"success" : "Done."}, 200

@app.route('/set_schema_name', methods=['POST'])
def set_schema_name():
    req = request.get_json()
    if req['type'] == 'resource':
        global RESOURCE_SCHEMA
        RESOURCE_SCHEMA = req['schemaName']
        gcf.Config(config_path).updateConfig('DATABASE-INFO', 'schemaName', req['schemaName'])
    
    elif req['type'] == 'detail':
        global DETAIL_SCHEMA
        DETAIL_SCHEMA = req['schemaName']
        gcf.Config(config_path).updateConfig('DATABASE-INFO', 'detailSchemaName', req['schemaName'])
    
    return 'ok'
        
@app.route('/source_to_target', methods=['POST'])
def source_to_target():
    db_source = read_conf()['DATABASE-INFO'].copy()
    cd = cda.Connect(db=db_source)
    table_list = [x['table_name'] for x in cd.query_db(f"show tables from {cd.db_name}.{db_source['schemaName']};") if x['type'] == 'table']

    result = {}
    for tbl in table_list:
        __tbl = cd.query_db(f"select * from {db_source['schemaName']}.{tbl};")
        result[tbl] = pd.DataFrame(__tbl).to_dict('split', index=False)

    json_res = json.dumps(result, default=str)
    
    try:
        requests.post(target_url+"/set_resource_info", 
                      data=json_res, 
                      headers={'Content-Type': 'application/json'}, 
                      timeout=0.0000000001)
    except requests.exceptions.ReadTimeout: 
        pass
    except requests.exceptions.ConnectTimeout:
        pass

    return json_res

@app.route('/set_resource_info', methods=['POST'])
def set_resource_info():
    req = request.get_json()
    global DETAIL_SCHEMA
    start_time = str(int(time.time() * 1000))
    detail_schema_name = "ds_" + start_time

    db_source = read_conf()['DATABASE-INFO'].copy()
    existence_db(db_source)
    create_resource_schema(db_source, detail_schema_name)
    db_source['schemaName'] = detail_schema_name
    param_obj = {'db_source' : db_source, 'req' : req, 'config_path' : config_path}

    with open(f"./{detail_schema_name}.pkl", 'wb') as file: 
        pickle.dump(param_obj, file)

    # req -> db
    subprocess.Popen([sys.executable or 'python', 'insertDetail.py', detail_schema_name])

    return {"success" : "Done."}, 200

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
    db_temp_path = "./db_temp.pkl"
    target_ip = read_conf()['DATABASE-INFO']['target']
    target_url = f"http://{target_ip}:9999"    # it is test ip for target

    RESOURCE_SCHEMA = read_conf()['DATABASE-INFO']['schemaName']
    DETAIL_SCHEMA = read_conf()['DATABASE-INFO']['detailSchemaName']

    cyclic_sync = subprocess.Popen([sys.executable or 'python', 'cyclicSync.py', status_path, config_path])
    atexit.register(cyclic_sync.kill)
    
    app.run(threaded=True, debug=True, host='0.0.0.0', port=9999)