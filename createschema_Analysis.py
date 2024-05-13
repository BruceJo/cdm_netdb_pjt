import connDbnApi as cda

class Create():
    def __init__(self, destination,aa):
        self.destination = destination

    def create_schema(self):
        conn = cda.Connect(db = self.destination).connect_cockroachdb()
        conn.autocommit = True
        cur = conn.cursor()
        #DB와 상호작용하기 위해 연결해주는 cur (cursor)객체
        q = f"CREATE SCHEMA IF NOT EXISTS {self.destination['schemaName']};"
        cur.execute(q) # db에 쿼리 넘겨줌   
        cur.close()
        conn.close()
    
    def create_table(self):
        conn = cda.Connect(db = self.destination).connect_cockroachdb()
        conn.autocommit = True
        cur = conn.cursor()
        with open(self.destination["schemaPath"], 'r') as file:
            sql = file.read()
        
        sql = sql.replace("CREATE TABLE ", f"CREATE TABLE {self.destination['schemaName']}.")
        sql = sql.replace("CREATE SEQUENCE IF NOT EXISTS ", f"CREATE SEQUENCE IF NOT EXISTS {self.destination['schemaName']}.")
        cur.execute(f"set schema {self.destination['schemaName']};")
        cur.execute(sql)
        cur.close()
        conn.close()
