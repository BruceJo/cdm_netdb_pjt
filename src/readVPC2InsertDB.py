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

    def setUrl(self, name, action):
        self.table_name = name.lower()
        nc = ncset.urlInfo()
        action = action[0].lower()
        if action == "c":
            self.api_url, self.sub_url = nc[name]["api_url"], nc[name]["create"]
        elif action == "r":
            self.api_url, self.sub_url = nc[name]["api_url"], nc[name]["read"]
        elif action == "u":
            self.api_url, self.sub_url = nc[name]["api_url"], nc[name]["update"]
        elif action == "d":
            self.api_url, self.sub_url = nc[name]["api_url"], nc[name]["delete"]

    def readDb(self):
        res = json.loads(self.cc.get_list(self.api_url, self.sub_url))
        print('res','\n',res)
        return res
    
    def insert_db(self, dict1):
        key_list = list(dict1.keys())
        key_str = (', '.join(key_list)).lower()
        val_list = list(dict1.values())
        
        query = f'INSERT INTO {self.destination["schemaName"]}.{self.table_name} ({key_str}) VALUES {tuple(val_list)};'
        print(query)
        # self.cur.execute(query)
    
    def insert_route(self):
        vpc_list = self.cc.query_db(f"select v.vpcno, r.routetableno, r.id from {self.destination['dbName']}.{self.destination['schemaName']}.vpc v, {self.destination['dbName']}.{self.destination['schemaName']}.routetable r where v.id = r.vpcid")
        for row in vpc_list:
            api_url, sub_url = 'vpc', 'getRouteList'
            res = json.loads(self.cc.get_route_list(api_url, sub_url, row['vpcno'], row['routetableno']))
            
            # loop
            for src in res[sub_url+"Response"][sub_url[3].lower()+sub_url[4:]]: 
                for i in src:
                    try:
                        if i in ['targetType']:
                            src[i] = src[i]['code']
                    except:
                        pass
            
                dict1 = {}
                dict1['routetableid'] = row['id']

                for key in src:
                    if key not in ['routeTableNo']:
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
        if self.table_name == 'inautoscalinggroupserverinstance':
            source = source[0]["inAutoScalingGroupServerInstanceList"]
        for src in source: 
            # modification
            _temp = {}
            for i in src:
                # Common
                # routetable : 'supportedSubnetType', 'routeTableStatus'
                # PlacementGroup : 'placementGroupType'
                # LaunchConfiguration : 'launchConfigurationStatus'
                # InAutoScalingGroupServerInstance : 'healthStatus', 'lifecycleState'
                # ServerInstance : 'platformType', 'serverInstanceStatus', 'serverInstanceOperation', 'serverInstanceType', 'baseBlockStorageDiskType', 'baseBlockStorageDiskDetailType'
                # MemberServerImage : 'memberServerImageInstanceStatus', 'memberServerImageInstanceOperation', 'shareStatus'
                if i in ['supportedSubnetType', 'routeTableStatus', 'placementGroupType', 'launchConfigurationStatus', 'healthStatus', 'lifecycleState', 
                         'platformType', 'serverInstanceStatus', 'serverInstanceOperation', 'serverInstanceType', 'baseBlockStorageDiskType', 'baseBlockStorageDiskDetailType',
                         'memberServerImageInstanceStatus', 'memberServerImageInstanceOperation', 'shareStatus']:
                    src[i] = src[i]['code']
                elif i in ['createDate', 'uptime']:
                    src[i] = src[i].replace('T',' ')
                    src[i] = src[i].replace('Z','')
                elif i in ['networkInterfaceNoList', 'sharedLoginIdList']:
                    src[i] = ','.join(src[i])
                elif i == 'vpcNo':
                    _temp[i] = self.get_id('vpc', 'vpcno', src[i])
                elif i == 'serverProductCode':
                    _temp[i] = self.get_id('product', 'productcode', src[i])
                elif i == 'loginKeyName':
                    _temp[i] = self.get_id('loginkey', 'keyname', src[i])
                elif i == 'zoneCode':
                    _temp[i] = self.get_id('zone', 'zonecode', src[i])
                elif i == 'regionCode':
                    _temp[i] = self.get_id('region', 'regioncode', src[i])
                elif i == 'vpcNo':
                    _temp[i] = self.get_id('vpc', 'vpcno', src[i])
                elif i == 'subnetNo':
                    _temp[i] = self.get_id('subnet', 'subnetno', src[i])
                   
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



            # filter columns
            out_candidate = dict(
                RouteTable = ['vpcNo', 'regionCode'],
                LaunchConfiguration = ['regionCode', 'serverProductCode', 'loginKeyName'],
                InAutoScalingGroupServerInstance = ['regionCode', 'serverProductCode', 'loginKeyName'],
                ServerInstance = ['serverProductCode', 'hypervisorType', 'serverImageNo', 'serverSpecCode', 'zoneCode', 'regionCode', 'vpcNo', 'subnetNo']
            )
            
            if self.table_name != 'serverinstance':
                out_field = list(set(sum([v for k,v in out_candidate.items() if k != 'ServerInstance'], [])))
            else:
                out_field = out_candidate['ServerInstance']
            
            for key in src:
                if key not in out_field:
                    if key in dict1:
                        dict1[key].append(src[key])
                    else:
                        dict1[key] = src[key]

            self.insert_db(dict1)

    def run(self):
        # 나중에 loop
        this = "ServerInstance"
        self.setUrl(this, "read")
        
        if this != "Route":
            read_data = self.readDb()
            # if read_data then 1dan / 2dan
            self.insert1dan(read_data)
        elif this == "Route":
            self.insert_route()