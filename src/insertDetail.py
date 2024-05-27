import main as m
import os
import sys
import pickle
import pandas as pd
import time
import requests
import json
import naverCloud
import connDbnApi as cda
import getConfig as gcf

if __name__ == '__main__':
    start = time.time()
    detail_schema_name = sys.argv[1]
    file_path = f"./{detail_schema_name}.pkl"
    with open(file_path, 'rb') as file: 
        args = pickle.load(file)
    db_source = args['db_source']
    req = args['req']
    config_path = args['config_path']
    if os.path.exists(file_path):
        os.remove(file_path)

    engine = m.insert_to_detail_engine(db_source)

    order_key_dict = naverCloud.url_info()
    order_key = [x.lower() for x in order_key_dict if x != 'Region'] + ['region']
    order_key = [x for x in order_key if x in req.keys()]

    for tbl_name in order_key:
        tbl_info = req[tbl_name]
        __temp = pd.DataFrame(**tbl_info)
        if __temp.empty != True:
            print("insert to ", tbl_name)
            __temp.to_sql(tbl_name, engine, schema=detail_schema_name, if_exists='replace', index=False)
            # try:
            #     __temp.to_sql(tbl_name, engine, schema=detail_schema_name, if_exists='replace', index=False)
            # except:
            #     # push error (★ RMQ 비동기 전달 -> NaverStop ★)
            #     pass
    
    # del ds_ schema
    cd = cda.Connect(db=db_source)
    schema_list = [x['schema_name'] for x in cd.query_db("show schemas;") if x['schema_name'][:3] == 'ds_']
    schema_list = [x for x in schema_list if x != detail_schema_name]
    last_schema = max(schema_list)
    
    if last_schema < detail_schema_name:
        response = requests.post("http://localhost:9999/set_schema_name",
                                 data=json.dumps({'type' : 'detail', 'schemaName' : detail_schema_name}),
                                 headers={'Content-Type': 'application/json'})

    cyclic = gcf.Config(config_path).getConfig()['CYCLIC-SYNC'].copy()
    retention_policy = int(cyclic['schemaRetentionPolicy'])
    schema_list = schema_list + [detail_schema_name]

    if len(schema_list) >= retention_policy:
        del_targets = sorted(schema_list, reverse=True)[retention_policy:]
        print('schema_list', schema_list)
        print('del_targets', del_targets)

        # https://github.com/cockroachdb/cockroach/issues/47790
        for del_target in del_targets:
            cd.delete_schema(del_target)

        print("Past schema deletion completed by retention policy.")