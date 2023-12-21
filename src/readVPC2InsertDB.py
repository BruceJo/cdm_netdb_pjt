import connCockroachDB as ccdb
import naverCloud as ncset
import json

# constant
regionid = 922761106863882241

class Read2Insert():
    def __init__(self, api, destination):
        self.destination = destination
        self.cc = ccdb.Connect(api=api, destination=destination)
        self.conn = self.cc.connect_cockroachdb()
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def set_url(self, name, action):
        self.table_name = name.lower()
        nc = ncset.url_info()
        action = action[0].lower()
        if action == "c":
            self.api_url, self.sub_url = nc[name]["api_url"], nc[name]["create"]
        elif action == "r":
            self.api_url, self.sub_url = nc[name]["api_url"], nc[name]["read"]
        elif action == "u":
            self.api_url, self.sub_url = nc[name]["api_url"], nc[name]["update"]
        elif action == "d":
            self.api_url, self.sub_url = nc[name]["api_url"], nc[name]["delete"]

    def read_db(self):
        res = json.loads(self.cc.get_list(self.api_url, self.sub_url))
        # print('res','\n',res)
        return res
    
    def insert_db(self, dict1):
        key_list = list(dict1.keys())
        key_str = (', '.join(key_list)).lower()
        val_list = list(dict1.values())
        
        query = f'INSERT INTO {self.destination["schemaName"]}.{self.table_name} ({key_str}) VALUES {tuple(val_list)};'
        print(query)
        # self.cur.execute(query)

    def insert_special(self, target):
        target = target.lower()
        info = ncset.special_info()

        from_body = f"{self.destination['dbName']}.{self.destination['schemaName']}."
        query_body = f"select {', '.join(info[target]['value'])} from {', '.join([from_body+x for x in info[target]['table']])}"
        where_body = ' where ' + ' and '.join([x for x in info[target]['where']]) if info[target]['where'] else ''
        condition_list = self.cc.query_db(query_body + where_body)

        for row in condition_list:
            fetch_body = eval("{" + ", ".join([f"'{k}':{v}" for k, v in info[target]['fetch'].items()]) + "}")
            res = json.loads(self.cc.get_list(self.api_url, self.sub_url, **fetch_body))
            
            # loop
            _temp = {}
            for src in res[self.sub_url+"Response"][info[target]['stage']]: 
                for i in src:
                    if i in ['targetType']:
                        src[i] = src[i]['code']
                    elif i in ['createDate', 'startTime', 'endTime']:
                        src[i] = src[i].replace('T',' ').replace('Z','')
                    elif i in ['actionStatus', 'ruleAction', 'networkAclRuleType', 'adjustmentType']:
                        src[i] = src[i]['code']
                    elif i == 'networkAclNo':
                        _temp[i] = self.get_id('networkacl', 'networkaclno', src[i])
                    elif i == 'protocolType':
                        if src[i] == 'TCP':
                            _temp[i] = 1
                        elif src[i] == 'UDP':
                            _temp[i] = 2
                        elif src[i] == 'ICMP':
                            _temp[i] = 3
                        else:
                            _temp[i] = 0

                dict1 = {}
                if self.table_name == 'route':
                    dict1['routetableid'] = row['id']
                elif self.table_name == 'networkaclrule':
                    dict1['networkaclid'] = _temp['networkAclNo']
                    dict1['protocolid'] = _temp['protocolType']
                elif self.table_name == ['activitylog', 'scalingpolicy', 'scheduledupdategroupaction']:
                    dict1['autoscalinggroupid'] = int(row['autoscalinggroupno'])

                for key in src:
                    if key not in ['routeTableNo', 'autoScalingGroupNo', 'regionCode', 'networkAclNo', 'protocolType', 'autoScalingGroupNo']:
                        if key in dict1:
                            dict1[key].append(src[key])
                        else:
                            dict1[key] = src[key]
            
                self.insert_db(dict1)

    def get_id(self, tbl, where, value):
        result = self.cc.query_db(f"SELECT id FROM {self.destination['schemaName']}.{tbl} where {where}='{value}';")
        return None if len(result) == 0 else result[0]['id']
    
    def insert1dan(self, res):
        source = res[self.sub_url+"Response"][self.sub_url[3].lower()+self.sub_url[4:]]
        print("source", source)
        if self.table_name == 'inautoscalinggroupserverinstance':
            source = source[0]["inAutoScalingGroupServerInstanceList"]
        for src in source: 
            # modification
            _temp = {}
            for i in src:
                # Common
                code_candidate = dict(
                    RouteTable = ['supportedSubnetType', 'routeTableStatus'],
                    PlacementGroup = ['placementGroupType'],
                    LaunchConfiguration = ['launchConfigurationStatus'],
                    InAutoScalingGroupServerInstance = ['healthStatus', 'lifecycleState'],
                    ServerInstance = ['platformType', 'serverInstanceStatus', 'serverInstanceOperation', 'serverInstanceType', 'baseBlockStorageDiskType', 'baseBlockStorageDiskDetailType'],
                    MemberServerImage = ['memberServerImageInstanceStatus', 'memberServerImageInstanceOperation', 'shareStatus'],
                    AutoScalingGroup = ['autoScalingGroupStatus', 'healthCheckType'],
                    NatGatewayInstance = ['natGatewayInstanceStatus', 'natGatewayInstanceOperation', 'natGatewayType'],
                    NetworkAcl = ['networkAclStatus'],
                    NetworkAclDenyAllowGroup = ['networkAclDenyAllowGroupStatus'],
                    Vpc = ['vpcStatus'],
                    Subnet = ['subnetStatus', 'subnetType', 'usageType']
                )

                if i in list(set(sum([v for k,v in code_candidate.items()], []))):
                    src[i] = src[i]['code']
                elif i in ['createDate', 'uptime']:
                    src[i] = src[i].replace('T',' ').replace('Z','')
                elif i in ['networkInterfaceNoList', 'sharedLoginIdList', 'targetGroupNoList', 'inAutoScalingGroupServerInstanceList', 'suspendedProcessList', 'accessControlGroupNoList']:
                    src[i] = ','.join(src[i])
                elif self.table_name != 'vpc' and i == 'vpcNo':
                    _temp[i] = self.get_id('vpc', 'vpcno', src[i])
                elif i == 'serverProductCode':
                    _temp[i] = self.get_id('product', 'productcode', src[i])
                elif i == 'loginKeyName':
                    _temp[i] = self.get_id('loginkey', 'keyname', src[i])
                elif i == 'zoneCode':
                    _temp[i] = self.get_id('zone', 'zonecode', src[i])
                elif i == 'regionCode':
                    _temp[i] = self.get_id('region', 'regioncode', src[i])
                elif self.table_name != 'subnet' and i == 'subnetNo':
                    _temp[i] = self.get_id('subnet', 'subnetno', src[i])
                elif i == 'networkAclNo':
                    _temp[i] = self.get_id('networkacl', 'networkaclno', src[i])
                elif i == 'originalServerInstanceNo':
                    _temp[i] = src[i]
                   
            dict1 = {}
            if self.table_name == 'routetable':
                dict1['regionid'] = regionid
                dict1['vpcid'] = _temp['vpcNo']
            elif self.table_name == 'launchconfiguration':
                dict1['regionid'] = regionid
                dict1['serverproductid'] = _temp['serverProductCode']
                dict1['loginkeyid'] = _temp['loginKeyName']
            elif self.table_name == 'serverinstance':
                dict1['serverproductcodeid'] = _temp['serverProductCode']
                dict1['zoneid'] = _temp['zoneCode']
                dict1['regionid'] = _temp['regionCode']
                dict1['vpcid'] = _temp['vpcNo']
                dict1['subnetid'] = _temp['subnetNo']
            elif self.table_name == 'memberserverimageinstance':
                dict1['originalserverinstanceid'] = _temp['originalServerInstanceNo']
            elif self.table_name == 'autoscalinggroup':
                dict1['vpcid'] = _temp['vpcNo']
                dict1['subnetid'] = _temp['subnetNo']
            elif self.table_name == 'natgatewayinstance':
                dict1['vpcid'] = _temp['vpcNo']
                dict1['subnetid'] = _temp['subnetNo']
            elif self.table_name == 'networkacl':
                dict1['vpcid'] = _temp['vpcNo']
            elif self.table_name == 'networkacldenyallowgroup':
                dict1['vpcid'] = _temp['vpcNo']
            elif self.table_name == 'vpc':
                dict1['regionid'] = regionid
            elif self.table_name == 'subnet':
                dict1['vpcid'] = _temp['vpcNo']
                dict1['zoneid'] = _temp['zoneCode']
                dict1['networkaclid'] = _temp['networkAclNo']

            # filter columns
            out_candidate = dict(
                RouteTable = ['vpcNo', 'regionCode'],
                LaunchConfiguration = ['regionCode', 'serverProductCode', 'loginKeyName'],
                InAutoScalingGroupServerInstance = ['regionCode', 'serverProductCode', 'loginKeyName'],
                ServerInstance = ['serverProductCode', 'hypervisorType', 'serverImageNo', 'serverSpecCode', 'zoneCode', 'regionCode', 'vpcNo', 'subnetNo'],
                MemberServerImageInstance = ['originalServerImageProductCode', 'originalServerInstanceNo', 'originalServerInstanceProductCode'],
                AutoScalingGroup = ['vpcNo', 'vpcName', 'zoneCode', 'subnetName', 'subnetNo'],
                NatGatewayInstance = ['vpcNo', 'vpcName', 'zoneCode', 'subnetName', 'subnetNo'],
                Vpc = ['regionCode'],
                Subnet = ['vpcNo', 'zoneCode']
            )
            
            if self.table_name == 'serverinstance':
                out_field = out_candidate['ServerInstance']
            elif self.table_name == 'vpc':
                out_field = out_candidate['Vpc']
            elif self.table_name == 'subnet':
                out_field = []
            else:
                out_field = list(set(sum([v for k,v in out_candidate.items() if k != 'ServerInstance'], [])))
            
            for key in src:
                if key not in out_field:
                    if key in dict1:
                        dict1[key].append(src[key])
                    else:
                        dict1[key] = src[key]

            self.insert_db(dict1)

    def run(self):
        # 나중에 loop
        this = "Route"
        self.set_url(this, "read")
        
        if this in ["Route", "ActivityLog", "NetworkAclRule", "ScalingPolicy", "ScheduledUpdateGroupAction"]:
            self.insert_special(this)
        else:
            read_data = self.read_db()
            # if read_data then 1dan / 2dan
            self.insert1dan(read_data)
        