import connDbnApi as cda
import getConfig as gcf
import createSchema as cs
import getHistory as gh
import configparser as parser
import os

# basedir = os.path.dirname(os.path.abspath(__file__))
# print("**********8",basedir)
# os.chdir(basedir) #basedir 변경

CONF_PATH = "../conf/app.conf"
app_conf = gcf.Config(CONF_PATH).getConfig()
destination = app_conf['DATABASE-SOURCE'].copy()

def CreateDB():
    destination = app_conf['DATABASE-SOURCE'].copy()
    conn = cda.Connect(db=destination).connect_cockroachdb()
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

def CreateSchema():
    #schemaName을 StartTime으로 세팅
    StartTime = str(gh.SetStartTimestamp())
    config = parser.ConfigParser()
    config.read(CONF_PATH,encoding='utf-8')
    config.set('DATABASE-SOURCE', 'schemaName', StartTime)
    with open(CONF_PATH, 'w') as configfile:
        config.write(configfile)

    # cock_create = cs.Create(source) 
    # cock_create.create_schema() 
    # cock_create.create_table()
    # return 'success'


# def create() :
#     source = app_conf['DATABASE-SOURCE'].copy()
#     
if __name__ == '__main__':
    CreateDB()
    CreateSchema()



