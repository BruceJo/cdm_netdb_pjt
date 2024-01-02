import connDbnApi as cda

class Create():
    def __init__(self, destination):
        self.destination = destination

    def create_schema(self):
        conn = cda.Connect(db = self.destination).connect_cockroachdb()
        conn.autocommit = True
        cur = conn.cursor()
        q = f"CREATE SCHEMA IF NOT EXISTS {self.destination['schemaName']};"
        cur.execute(q)        
        cur.close()
        conn.close()
    
    def create_table(self):
        conn = cda.Connect(db = self.destination).connect_cockroachdb()
        conn.autocommit = True
        cur = conn.cursor()
        with open(self.destination["schemaPath"], 'r') as file:
            sql = file.read()
        
        sql = sql.replace("CREATE TABLE ", f"CREATE TABLE {self.destination['schemaName']}.")
        cur.execute(f"set schema {self.destination['schemaName']};")
        cur.execute(sql)
        # for s in sql.split(';')[:-1]:
        #     cur.execute(s+';')
        cur.close()
        conn.close()