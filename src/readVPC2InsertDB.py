import connDbnApi as cda
import naverCloud
import json

class Read2Insert():
    def __init__(self, api, destination):
        self.destination = destination
        self.cc = cda.Connect(api=api, db=destination)
        self.conn = self.cc.connect_cockroachdb()
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
        self.nc = naverCloud.url_info()
        self.code_candidate = naverCloud.code_candidate()
        self.out_candidate = naverCloud.out_candidate()
        self.col_name_mapper = naverCloud.col_name_mapper()
        self.special_info = naverCloud.special_info()
        self.init_table_rows = naverCloud.init_table_rows()
        self.special_table = [x.lower() for x in ['Route', 'ActivityLog', 'NetworkAclRule', 'ScalingPolicy', 'ScheduledUpdateGroupAction', 
                              'AccessControlGroupRule', 'LoadBalancerListener', 'LoadBalancerRule', 'LoadBalancerRuleAction',
                              'LoadBalancerRuleCondition']]
        self.continue_flag = False

    def set_url(self, name, action):
        self.table_name, self.api_url, self.sub_url = naverCloud.set_url(name, action)

    def read_api(self):
        res = self.cc.request_api(self.api_url, self.sub_url)
        return res
    
    def insert_db(self, dict1):
        if self.continue_flag:
            self.continue_flag = False
            return None
        
        dict1 = {k: v for k, v in dict1.items() if v is not None}   # None -> null from (TBL)loadbalancersubnet/(COL)publicipinstanceid
        dict1 = {k: (json.dumps(v) if (type(v)==list) else v) for k, v in dict1.items()}       # list(dict()) -> str() w/ ' string
        dict1 = {k: (v.replace("'", "''") if (type(v)==str and "'" in v) else v) for k, v in dict1.items()}     # escape ' -> ''

        key_list = list(dict1.keys())
        key_str = (', '.join(key_list)).lower()
        val_tuple = tuple(dict1.values())
        val_str = ', '.join(f"'{x}'" if isinstance(x, str) else str(x) for x in val_tuple)
        
        query = f'INSERT INTO {self.destination["schemaName"]}.{self.table_name} ({key_str}) VALUES ({val_str});'
        # print('3. query\n', query, '\n')
        with open("insert_query.log", "a") as file:
            file.write(query+'\n')
            file.close()
        self.cur.execute(query)

    def get_id(self, tbl, where, value):
        result = self.cc.query_db(f"SELECT id FROM {self.destination['schemaName']}.{tbl} where {where}='{value}';")
        return None if len(result) == 0 else result[0]['id']

    def proc_special(self, src):
        _temp = {}
        for i in src:   # instance
            if i in ['createDate', 'startTime', 'endTime']:
                src[i] = src[i].replace('T',' ').replace('Z','')
            elif i == 'routeTableNo':
                _temp[i] = self.get_id('routetable', 'routetableno', src[i])
            elif i == 'networkAclNo':
                _temp[i] = self.get_id('networkacl', 'networkaclno', src[i])
            elif i == 'accessControlGroupNo':
                _temp[i] = self.get_id('accesscontrolgroup','accesscontrolgroupno', src[i])
            elif i == 'loadBalancerInstanceNo':
                _temp[i] = self.get_id('loadbalancerinstance', 'loadbalancerinstanceno', src[i])
            elif i == 'loadBalancerListenerNo':
                _temp[i] = self.get_id('loadbalancerlistener', 'loadbalancerlistenerno', src[i])
            elif self.table_name != 'loadbalancerlistener' and i == 'protocolType':
                _temp[i] = self.get_id('protocoltype', 'codename', src[i]['codeName'])
            elif i == 'autoScalingGroupNo':
                _temp[i] = self.get_id('autoscalinggroup', 'autoscalinggroupno', src[i])
            # protocolType 으로 인하여 고의적 하단 위치
            elif i in ['targetType', 'actionStatus', 'ruleAction', 'networkAclRuleType', 'adjustmentType', 'accessControlGroupRuleType', 'protocolType', 'ruleActionType', 'ruleConditionType']:
                src[i] = src[i]['code']
            elif i in ['loadBalancerRuleNoList', 'cipherSuiteList']:
                pass
            elif i == 'tlsMinVersionType':
                src[i] = src[i]['code'] if 'code' in src[i] else ''
        
        dict1 = {}
        if self.table_name == 'route':
            dict1['routetableid'] = _temp['routeTableNo']
        elif self.table_name == 'networkaclrule':
            dict1['networkaclid'] = _temp['networkAclNo']
            dict1['protocolid'] = _temp['protocolType']
        elif self.table_name in ['activitylog', 'scalingpolicy', 'scheduledupdategroupaction']:
            dict1['autoscalinggroupid'] = _temp['autoScalingGroupNo']
        elif self.table_name == 'accesscontrolgrouprule':
            dict1['accesscontrolgroupid'] = _temp['accessControlGroupNo']
            dict1['protocoltypeid'] = _temp['protocolType']
        elif self.table_name == 'loadbalancerlistener':
            dict1['loadbalancerinstanceid'] = _temp['loadBalancerInstanceNo']
        elif self.table_name == 'loadbalancerrule':
            dict1['loadbalancerlistenerid'] = _temp['loadBalancerListenerNo']

        if self.table_name == 'loadbalancerruleaction':
            if 'redirectionAction' in src:
                dict1['redirectionAction'] = json.dumps(src['redirectionAction'])
            else:
                dict1['redirectionAction'] = None

            if 'targetGroupAction' in src:
                dict1['targetGroupAction'] = json.dumps(src['targetGroupAction'])
            else:
                dict1['targetGroupAction'] = None

        if self.table_name == 'loadbalancerrulecondition':
            dict1['hostheadercondition'] = '' # 이 예제에서는 redirectionaction에 대한 데이터가 JSON에 없으므로 빈 문자열 사용
            if 'pathPatternCondition' in src:
                dict1['pathpatterncondition'] = json.dumps(src['pathPatternCondition'])
            else:
                dict1['pathpatterncondition'] = None



        for key in src:
            if self.table_name != 'loadbalancerlistener':
                out_candidate = ['routeTableNo', 'autoScalingGroupNo', 'regionCode', 'networkAclNo', 'protocolType', 'autoScalingGroupNo', 'accessControlGroupNo', 'loadBalancerListenerNo',
                                 'pathPatternCondition', 'targetGroupAction', 'redirectionAction']
            else:
                out_candidate = ['loadBalancerInstanceNo']
            
            if key not in out_candidate:
                if key in dict1:
                    dict1[key].append(src[key])
                else:
                    dict1[key] = src[key]
    
        self.insert_db(dict1)

    def proc_normal(self, src):
        _temp = {}
        for i in src:
            # Common
            if i in list(set(sum([v for k,v in self.code_candidate.items()], []))):
                src[i] = src[i]['code']
            elif i in ['createDate', 'uptime']:
                src[i] = src[i].replace('T',' ').replace('Z','')
            elif self.table_name != 'autoscalinggroup' and i in ['networkInterfaceNoList', 'sharedLoginIdList', 'targetGroupNoList', 
                        'inAutoScalingGroupServerInstanceList', 'suspendedProcessList', 'accessControlGroupNoList', 'secondaryIpList', 
                        'loadBalancerIpList', 'subnetNoList', 'loadBalancerListenerNoList', 'loadBalancerSubnetList', 'ipList']:
                pass
            elif self.table_name not in ['vpc', 'accesscontrolgroup'] and i == 'vpcNo':
                _temp[i] = self.get_id('vpc', 'vpcno', src[i])
            elif self.table_name != 'product' and i == 'serverProductCode':
                _temp[i] = self.get_id('product', 'productcode', src[i])
            elif self.table_name != 'serverinstance' and i == 'loginKeyName':
                _temp[i] = self.get_id('loginkey', 'keyname', src[i])
            elif self.table_name not in ['natgatewayinstance', 'zone'] and i == 'zoneCode':
                _temp[i] = self.get_id('zone', 'zonecode', src[i])
            elif self.table_name != 'region' and i == 'regionCode':
                _temp[i] = self.get_id('region', 'regioncode', src[i])
            elif self.table_name != 'subnet' and i == 'subnetNo':
                _temp[i] = self.get_id('subnet', 'subnetno', src[i])
            elif self.table_name != 'networkacl' and i == 'networkAclNo':
                _temp[i] = self.get_id('networkacl', 'networkaclno', src[i])
            elif i == 'originalBlockStorageInstanceNo':
                _temp[i] = src[i]
            #    _temp[i] = self.get_id('blockstorageinstance', 'blockstorageinstanceno', src[i])
            #    if _temp[i] == None: self.continue_flag = True
            elif i in ['targetVpcNo', 'sourceVpcNo']:
                _temp[i] = self.get_id('vpc', 'vpcno', src[i])
            elif self.table_name not in ['publicipinstance', 'serverinstance', 'natgatewayinstance'] and i == 'publicIpInstanceNo':
                _temp[i] = self.get_id('publicipinstance', 'publicipinstanceno', src[i])
            elif i == 'originalServerInstanceNo':
                _temp[i] = src[i]
            elif i in ['productItemKind', 'targetType', 'targetGroupProtocolType', 'algorithmType', 'healthCheckProtocolType', 'healthCheckHttpMethodType']:
                if 'code' not in src[i]:
                    _temp[i] = 'null' #code가 비어있을 때 있음
                else:
                    _temp[i] = src[i]['code']                
        
        dict1 = {}
        for k, v in _temp.items():
            try:
                dict1[self.col_name_mapper['common'][k]] = _temp[k]
            except KeyError:
                dict1[self.col_name_mapper[self.table_name][k]] = _temp[k]
        
        if self.table_name == 'product':
            dict1['infraresourcetype'] = '' # 이 예제에서는 infraresourcetype에 대한 데이터가 JSON에 없으므로 빈 문자열 사용

        # filter columns
        except_tables = ['region', 'zone', 'serverinstance', 'vpc', 'vpcpeeringinstance', 'subnet', 'natgatewayinstance']
        if self.table_name in except_tables:
            out_field = self.out_candidate[self.table_name]
        elif self.table_name in ['accesscontrolgroup', 'publicipinstance']:
            out_field = []
        else:
            out_field = list(set(sum([v for k,v in self.out_candidate.items() if k not in except_tables], [])))

        for key in src:
            if (key not in out_field) and (key not in dict1):
                dict1[key] = src[key]
        
        self.insert_db(dict1)

    def insert_special(self, target):
        target = target.lower()
        from_body = f"{self.destination['dbName']}.{self.destination['schemaName']}."
        query_body = f"select {', '.join(self.special_info[target]['value'])} from {', '.join([from_body+x for x in self.special_info[target]['table']])}"
        where_body = ' where ' + ' and '.join([x for x in self.special_info[target]['where']]) if self.special_info[target]['where'] else ''
        condition_list = self.cc.query_db(query_body + where_body)

        for row in condition_list:
            fetch_body = eval("{" + ", ".join([f"'{k}':{v}" for k, v in self.special_info[target]['fetch'].items()]) + "}")
            res = self.cc.request_api(self.api_url, self.sub_url, **fetch_body)
            source = res[self.sub_url+"Response"][self.special_info[target]['stage']]

            # loop
            for src in source:  # loadBalancerRuleList
                if self.table_name == 'loadbalancerruleaction':
                    for instance in src['loadBalancerRuleActionList']:
                        self.proc_special(instance)
                elif self.table_name == 'loadbalancerrulecondition':
                    for instance in src['loadBalancerRuleConditionList']:
                        self.proc_special(instance)
                else:
                    self.proc_special(src)
    
    def run_insert(self, res):
        source = res[self.sub_url+"Response"][self.sub_url[3].lower()+self.sub_url[4:]]
        
        for src in source:
            if self.table_name == 'inautoscalinggroupserverinstance':
                for instance in src['inAutoScalingGroupServerInstanceList']:
                    self.proc_normal(instance)
            elif self.table_name == 'loadbalancersubnet':
                for instance in src['loadBalancerSubnetList']:
                    self.proc_normal(instance)
            else:
                self.proc_normal(src)

    def init_table(self):
        self.table_name = 'protocoltype'
        for _dict in self.init_table_rows[self.table_name]: self.insert_db(_dict)

    def run(self):
        self.init_table()

        # this = 'NetworkAclRule'
        for this in self.nc.keys():
            self.set_url(this, "read")
            with open("insert_query.log", "a") as file:
                file.write('>>>> table_name : ' + self.table_name + '\n')
                file.close()
            
            if self.table_name in self.special_table:
                self.insert_special(self.table_name)
            else:
                read_data = self.read_api()
                self.run_insert(read_data)
