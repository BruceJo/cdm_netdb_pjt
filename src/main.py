from flask import Flask, request, Response
from flask_cors import CORS
import json
# import requests
import getConfig as gcf
import createDB
import readVPC2InsertDB as rv2

#Flask init
app = Flask(__name__)
CORS(app)

@app.route('/create_db', methods=['POST'])
def create_db():
    # request format
    # {
    #     "dbName" : "cdm_fix",
    #     "schemaName" : "{some_resource_name}",
    #     "host" : "211.188.69.4",
    #     "port" : "26257",
    #     "user" : "root"
    # }
    req = request.get_json()
    source = app_conf['SOURCE-NAVER-CLOUD']
    
    for k, v in req.items():
        source[k] = v
    
    cock_create = createDB.Create(source)
    cock_create.create_schema()
    cock_create.create_table()

    return 'sucess'

@app.route('/read2insert', methods=['POST'])
def read2insert():
    #req = request.get_json()
    api = app_conf['API']
    source = app_conf['SOURCE-NAVER-CLOUD']
    
    # for k, v in req.items():
    #     source[k] = v
    
    ri = rv2.Read2Insert(api, source)
    ri.run()

    return 'sucess'



#Server Run
if __name__ == '__main__':
    CONF_PATH = "../conf/app.conf"
    app_conf = gcf.Config(CONF_PATH).getConfig()
    
    app.run(threaded=True, debug=True, host='0.0.0.0', port=9999)