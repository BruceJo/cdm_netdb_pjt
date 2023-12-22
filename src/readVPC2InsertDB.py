import connCockroachDB as ccdb
import naverCloud as ncset

class Read2Insert():
    def __init__(self, api, destination):
        self.destination = destination
        self.cc = ccdb.Connect(api=api, destination=destination)
        self.conn = self.cc.connect_cockroachdb()
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
        self.nc = ncset.url_info()
        self.code_candidate = ncset.code_candidate()
        self.out_candidate = ncset.out_candidate()
        self.col_name_mapper = ncset.col_name_mapper()
        self.special_info = ncset.special_info()

    def set_url(self, name, action):
        self.table_name = name.lower()
        action = action[0].lower()
        if action == "c":
            self.api_url, self.sub_url = self.nc[name]["api_url"], self.nc[name]["create"]
        elif action == "r":
            self.api_url, self.sub_url = self.nc[name]["api_url"], self.nc[name]["read"]
        elif action == "u":
            self.api_url, self.sub_url = self.nc[name]["api_url"], self.nc[name]["update"]
        elif action == "d":
            self.api_url, self.sub_url = self.nc[name]["api_url"], self.nc[name]["delete"]

    def read_db(self):
        res = self.cc.get_list(self.api_url, self.sub_url)
        # print('res','\n',res)
        return res
    
    def insert_db(self, dict1):
        key_list = list(dict1.keys())
        key_str = (', '.join(key_list)).lower()
        val_list = list(dict1.values())
        
        query = f'INSERT INTO {self.destination["schemaName"]}.{self.table_name} ({key_str}) VALUES {tuple(val_list)};'
        print(query)
        # with open("change_origin.txt", "a") as file:
        #     file.write(query+'\n')
        #     file.close()
        # self.cur.execute(query)

    def insert_special(self, target):
        target = target.lower()
        from_body = f"{self.destination['dbName']}.{self.destination['schemaName']}."
        query_body = f"select {', '.join(self.special_info[target]['value'])} from {', '.join([from_body+x for x in self.special_info[target]['table']])}"
        where_body = ' where ' + ' and '.join([x for x in self.special_info[target]['where']]) if self.special_info[target]['where'] else ''
        condition_list = self.cc.query_db(query_body + where_body)

        for row in condition_list:
            fetch_body = eval("{" + ", ".join([f"'{k}':{v}" for k, v in self.special_info[target]['fetch'].items()]) + "}")
            res = self.cc.get_list(self.api_url, self.sub_url, **fetch_body)
            # print(res)

            # loop
            _temp = {}
            for src in res[self.sub_url+"Response"][self.special_info[target]['stage']]: 
                for i in src:
                    if i in ['targetType']:
                        src[i] = src[i]['code']
                    elif i in ['createDate', 'startTime', 'endTime']:
                        src[i] = src[i].replace('T',' ').replace('Z','')
                    elif i in ['actionStatus', 'ruleAction', 'networkAclRuleType', 'adjustmentType', 'accessControlGroupRuleType']:
                        src[i] = src[i]['code']
                    elif i == 'networkAclNo':
                        _temp[i] = self.get_id('networkacl', 'networkaclno', src[i])
                    elif i == 'accessControlGroupNo':
                        _temp[i] = self.get_id('accesscontrolgroup','accesscontrolgroupno', src[i])
                    elif i == 'protocolType':
                        _temp[i] = self.get_id('protocoltype', 'codename', src[i]['codeName'])

                dict1 = {}
                if self.table_name == 'route':
                    dict1['routetableid'] = row['id']
                elif self.table_name == 'networkaclrule':
                    dict1['networkaclid'] = _temp['networkAclNo']
                    dict1['protocolid'] = _temp['protocolType']
                elif self.table_name in ['activitylog', 'scalingpolicy', 'scheduledupdategroupaction']:
                    dict1['autoscalinggroupid'] = int(row['autoscalinggroupno'])
                elif self.table_name == 'accesscontrolgrouprule':
                    dict1['accesscontrolgroupid'] = _temp['accessControlGroupNo']
                    dict1['protocoltypeid'] = _temp['protocolType']

                for key in src:
                    if key not in ['routeTableNo', 'autoScalingGroupNo', 'regionCode', 'networkAclNo', 'protocolType', 'autoScalingGroupNo', 'accessControlGroupNo']:
                        if key in dict1:
                            dict1[key].append(src[key])
                        else:
                            dict1[key] = src[key]
            
                self.insert_db(dict1)

    def get_id(self, tbl, where, value):
        result = self.cc.query_db(f"SELECT id FROM {self.destination['schemaName']}.{tbl} where {where}='{value}';")
        return None if len(result) == 0 else result[0]['id']
    
    def run_insert(self, res):
        source = res[self.sub_url+"Response"][self.sub_url[3].lower()+self.sub_url[4:]]
        print('source', source)

        if self.table_name == 'inautoscalinggroupserverinstance':
            source = source[0]['inAutoScalingGroupServerInstanceList']
        for src in source: 
            # modification
            _temp = {}
            for i in src:
                # Common
                if i in list(set(sum([v for k,v in self.code_candidate.items()], []))):
                    src[i] = src[i]['code']
                elif i in ['createDate', 'uptime']:
                    src[i] = src[i].replace('T',' ').replace('Z','')
                elif i in ['networkInterfaceNoList', 'sharedLoginIdList', 'targetGroupNoList', 'inAutoScalingGroupServerInstanceList', 
                           'suspendedProcessList', 'accessControlGroupNoList', 'accessControlGroupNoList', 'secondaryIpList']:
                    src[i] = ','.join(src[i])
                elif self.table_name not in ['vpc', 'accesscontrolgroup'] and i == 'vpcNo':
                    _temp[i] = self.get_id('vpc', 'vpcno', src[i])
                elif self.table_name != 'product' and i == 'serverProductCode':
                    _temp[i] = self.get_id('product', 'productcode', src[i])
                elif self.table_name != 'serverinstance' and i == 'loginKeyName':
                    _temp[i] = self.get_id('loginkey', 'keyname', src[i])
                elif self.table_name != 'natgatewayinstance' and i == 'zoneCode':
                    _temp[i] = self.get_id('zone', 'zonecode', src[i])
                elif i == 'regionCode':
                    _temp[i] = self.get_id('region', 'regioncode', src[i])
                elif self.table_name != 'subnet' and i == 'subnetNo':
                    _temp[i] = self.get_id('subnet', 'subnetno', src[i])
                elif self.table_name != 'networkacl' and i == 'networkAclNo':
                    _temp[i] = self.get_id('networkacl', 'networkaclno', src[i])
                elif i == 'originalBlockStorageInstanceNo':
                    _temp[i] = self.get_id('blockstorageinstance', 'blockstorageinstanceno', src[i])
                elif i == 'originalServerInstanceNo':
                    _temp[i] = src[i]
                elif i == 'productItemKind':
                    _temp[i] = src[i]['code']
                elif i in ['targetVpcNo', 'sourceVpcNo']:
                    _temp[i] = self.get_id('vpc', 'vpcno', src[i])
                   
            dict1 = {}
            for k, v in _temp.items():
                try:
                    dict1[self.col_name_mapper['common'][k]] = _temp[k]
                except KeyError:
                    dict1[self.col_name_mapper[self.table_name][k]] = _temp[k]
            
            if self.table_name == 'product':
                dict1['infraresourcetype'] = '' # 이 예제에서는 infraresourcetype에 대한 데이터가 JSON에 없으므로 빈 문자열 사용
            
            # filter columns
            except_tables = ['serverinstance', 'vpc', 'vpcpeeringinstance']
            if self.table_name in except_tables:
                out_field = self.out_candidate[self.table_name]
            elif self.table_name in ['subnet', 'accesscontrolgroup']:
                out_field = []
            else:
                out_field = list(set(sum([v for k,v in self.out_candidate.items() if k not in except_tables], [])))

            for key in src:
                if (key not in out_field) and (key not in dict1):
                    dict1[key] = src[key]

            self.insert_db(dict1)

    def run(self):
        this = 'InitScript'
        # for this in self.nc.keys():
        self.set_url(this, "read")
        
        if this in ['Route', 'ActivityLog', 'NetworkAclRule', 'ScalingPolicy', 'ScheduledUpdateGroupAction', 'AccessControlGroupRule']:
            self.insert_special(this)
        else:
            read_data = self.read_db()
            self.run_insert(read_data)
        