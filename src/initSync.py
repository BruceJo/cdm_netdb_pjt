import connDbnApi as cda
import getConfig as gcf
import createSchema as cs
import getHistory as gh
import configparser as parser
import os
import readVPC2InsertDB as rv2
import subprocess
from subprocess import PIPE

CONF_PATH = "../conf/app.conf"
RunStatus = False
initFlag = False

def CreateDB():
    app_conf = gcf.Config(CONF_PATH).getConfig()
    destination = app_conf['DATABASE-SOURCE'].copy()
    print("#$%#$%#$%#$%345",destination)
    a=cda.Connect(db=destination)
    conn = a.connect_cockroachdb()
    conn.autocommit = True
    cur = conn.cursor()
    q = f"SHOW DATABASES;"
    cur.execute(q)
    databases = cur.fetchall() #db의 이름을 리스트 (안에 요소는 튜플) 로 반환

    databaseName = []
    for database in databases:
        databaseName.append(database[0])
    if 'cdm' not in databaseName: #cdm db가 있는지 확인하고
        q = f"CREATE DATABASE cdm;" #없다면 생성하기
        cur.execute(q)

    cur.close()
    conn.close()


def SetSchemaName():
    #schemaName을 StartTime으로 세팅
    StartTime = str(gh.SetStartTimestamp())
    print("StartTime : ",StartTime)
    config = parser.ConfigParser()
    config.read(CONF_PATH,encoding='utf-8')
    config.set('DATABASE-SOURCE', 'schemaName', StartTime)
    with open(CONF_PATH, 'w') as configfile:
        config.write(configfile)

def CreateSchema():

    SetSchemaName()

    app_conf = gcf.Config(CONF_PATH).getConfig()
    destination = app_conf['DATABASE-SOURCE'].copy()

    cock_create = cs.Create(destination)
    cock_create.create_schema() 
    cock_create.create_table()
    return 'success'

def RunSubprocess():
    interpreter = "C://Users//yubin//AppData//Local//Programs//Python//Python312//python.exe"
    process = subprocess.Popen([interpreter,'getHistory.py'], shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    initFlag = True
    return process.pid


if __name__ == '__main__':
    if not RunStatus:
        print('error : not found subprocess')
        CreateDB() #지금 db에 접근이 안됨
        CreateSchema()
        #Insertinfo (질문필요)
        insert_error = False #일단 insert 성공했다고 가정
    if not insert_error:
        SetSchemaName()
        process_id = RunSubprocess()



