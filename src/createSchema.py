import connDbnApi as cda

class Create():
    def __init__(self, destination):
        self.destination = destination

    def create_schema(self):
        conn = cda.Connect(db = self.destination).connect_cockroachdb()
        conn.autocommit = True
        cur = conn.cursor()
        q = f'CREATE SCHEMA IF NOT EXISTS {self.destination["schemaName"]};'
        cur.execute(q)
        cur.close()
        conn.close()
    
    def create_table(self):
        conn = cda.Connect(db = self.destination).connect_cockroachdb()
        conn.autocommit = True
        cur = conn.cursor()
        with open(self.destination["schemaPath"], 'r', encoding='UTF8') as file:
            sql = file.read()
        
        sql = sql.replace('CREATE TABLE IF NOT EXISTS', f'CREATE TABLE IF NOT EXISTS "{self.destination["schemaName"]}".')
        sql = sql.replace('CREATE SEQUENCE IF NOT EXISTS ', f'CREATE SEQUENCE IF NOT EXISTS "{self.destination["schemaName"]}".')
        print(f'set schema {self.destination["schemaName"]};')
        cur.execute(f'set schema {self.destination["schemaName"]};')
        cur.execute(sql)
        cur.close()
        conn.close()
