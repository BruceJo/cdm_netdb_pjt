import connDbnApi as cda
import getConfig as gcf
import createSchema as cs

CONF_PATH = "../conf/app.conf"
app_conf = gcf.Config(CONF_PATH).getConfig()


def createDB():
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
    if 'cdm' not in databaseName:
        q1 = f"CREATE DATABASE cdm;"
        cur.execute(q1)
        print("\ncreate cdm!")

    cur.close()
    conn.close()

def create() :
    source = app_conf['DATABASE-SOURCE'].copy()
    cock_create = cs.Create(source) 
    cock_create.create_schema() 
    cock_create.create_table()
    return 'success'

# if __name__ == '__main__':
#     #createDB()



