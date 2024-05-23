import sys
import time
import requests
import json
import getConfig as gcf
import main as m
import readVPC2InsertDB as rv2
import connDbnApi as cda

def write_status(stat):
    # stat : init, idle, run
    with open(status_path, 'w') as sts:
        sts.write(stat)

def read_conf():   
    return gcf.Config(config_path).getConfig()

if __name__ == '__main__':
    HEADER = {'Content-Type': 'application/json'}
    status_path = sys.argv[1]
    config_path = sys.argv[2]
    binary_path = sys.argv[3]

    # diff_json = json.load(sys.argv[4])
    # print(diff_json)
    # RMQ 비동기 전달 -> NaverStop

    write_status('run')
    start_time = str(int(time.time() * 1000))
    resource_schema_name = "rs_" + start_time

    db_source = read_conf()['DATABASE-INFO'].copy()
    m.create_resource_schema(db_source, resource_schema_name)
    db_source['schemaName'] = resource_schema_name

    api = read_conf()['API-SOURCE-NAVER-CLOUD'].copy()
    ri = rv2.Read2Insert(api, db_source)
    # try:
    #     ri.run()
    # except:
    #     return {"error" : "insert error."}, 500

    cd = cda.Connect(db=db_source)
    schema_list = [x['schema_name'] for x in cd.query_db("show schemas;") if x['schema_name'][:3] == 'rs_']
    last_schema = max(schema_list)
    
    if last_schema < resource_schema_name:
        response = requests.post("http://localhost:9999/set_schema_name",
                                 data=json.dumps({'schemaName' : resource_schema_name}),
                                 headers=HEADER)
        # get resouece_info_from_db
        # push resource_info_from_db (RMQ 비동기 전달 -> NaverStop)

    cyclic = read_conf()['CYCLIC-SYNC'].copy()
    print(cyclic, schema_list)
    retention_policy = int(cyclic['schemaRetentionPolicy'])
    if len(schema_list) >= retention_policy:
        del_targets = sorted(schema_list, reverse=True)[retention_policy:]
        for del_target in del_targets:
            cd.delete_schema(del_target)
            
    write_status('idle')
