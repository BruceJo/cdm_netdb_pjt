import connDbnApi as cda
import naverCloud
import json

class CreateAll:
    def __init__(self, source_db, target_api):
        self.source_db = source_db
        self.target_api = target_api
        self.nc = naverCloud.url_info()
        self.include_keys = naverCloud.include_keys()
        self.cc = cda.Connect(api=target_api, db=source_db)
        self.conn = self.cc.connect_cockroachdb()
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def read_db(self, api_url, sub_url):
        res = self.cc.request_api(api_url, sub_url)
        return res

    def pretty_dict(self, _dict):
        return json.dumps(_dict, sort_keys=True, indent=4)

    def set_url(self, name, action):
        self.table_name, self.api_url, self.sub_url = naverCloud.set_url(name, action)

    def get_table(self, table_name):
        result = self.cc.query_db(f"SELECT * FROM {self.source_db['schemaName']}.{table_name};")
        return None if len(result) == 0 else result

    def get_value(self, _value: str, _from: str, **_where: dict):
        query_body = f"SELECT {_value} FROM {self.source_db['schemaName']}.{_from}"
        check_str = lambda x: f"'{x}'" if isinstance(x, str) else x
        check_bool = lambda x: str(x).lower() if isinstance(x, bool) else x
        where_list = [f"{k}={check_bool(check_str(v))}" for k, v in _where.items()]
        query_body += " where " + " and ".join(where_list) + ';' if where_list else query_body + ';'
        result = self.cc.query_db(query_body)
        return None if len(result) == 0 else result[0][_value]

    def create(self, row_dict, resource_type):
        print('1. row_dict\n', row_dict, '\n')
        print('2. include_keys\n', self.include_keys[self.table_name], '\n')

        dict1 = {}
        for key in self.include_keys[self.table_name]:
            # The logic to transform the information from the Source table appropriately
            # Add here the transformation logic for each key
            # Example:
            if key == 'exampleKey':
                value = self.get_value('columnName', 'tableName', **{'id': row_dict['rowId']})
                dict1.update({key: value})
            # Add similar logic for other keys

        dict1 = {k: v for k, v in dict1.items() if v is not None}
        print('3. body\n', self.pretty_dict(dict1), '\n')
        result = self.cc.request_api(self.api_url, self.sub_url, **dict1)
        print('4. request result\n', self.pretty_dict(result), '\n')

        if 'responseError' in result:
            raise Exception("[ERR] " + str(result))
        else:
            return dict1
        
    def create_resources(self):
        for resource_type in self.nc.keys():
            try:
                self.set_url(resource_type, "create")
                rows = self.get_table(self.table_name)
                for row in rows:
                    self.create(row, resource_type)  # Assuming 'create' is a method that handles the creation logic
            except Exception as e:
                print(f"Error in creating resource {resource_type}: {e}")

    def run(self):
        for resource_type in self.nc.keys():
            try:
                self.set_url(resource_type, "create")
                rows = self.get_table(self.table_name)
                for row in rows:
                    self.create(row, resource_type)
                    print(f"Created {resource_type}: {row}")
            except Exception as e:
                print(f"Error creating {resource_type}: {e}")

            try:
                self.set_url(resource_type, "read")
                read_result = self.read_db(self.api_url, self.sub_url)
                print(f"Read after creation for {resource_type}:\n{self.pretty_dict(read_result)}")
            except KeyError:
                print(f"No read operation defined for {resource_type}")

        # self.handle_dependencies()
        # self.log_creation_outcomes()

# Usage Example
if __name__ == "__main__":
    source_db_config = {}  # Your source DB configuration
    target_api_config = {}  # Your target API configuration
    create_all = CreateAll(source_db_config, target_api_config)
    create_all.run()
