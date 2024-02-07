import connDbnApi as cda
import naverCloud
import json

class Create():
    def __init__(self, source_db, target_api):
        self.source_db = source_db
        self.target_api = target_api
        self.nc = naverCloud.url_info()
        self.include_keys = naverCloud.include_keys()
        self.cc = cda.Connect(api=target_api, db=source_db)
        self.conn = self.cc.connect_cockroachdb()
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def read_db(self):
        res = self.cc.request_api(self.api_url, self.sub_url)
        
        return res

    def pretty_dict(self, _dict: dict):
        return json.dumps(_dict, sort_keys=True, indent=4)
        
    
    def set_url(self, name, action):
        self.table_name, self.api_url, self.sub_url = naverCloud.set_url(name, action)
        
    def get_table(self):
        result = self.cc.query_db(f"SELECT * FROM {self.source_db['schemaName']}.{self.table_name};")
        return None if len(result) == 0 else result

    def get_value(self, _value: str, _from: str, **_where: dict):
        # usage -> self.get_value(['col1', 'col2'], 'tbl')
        # usage -> self.get_value(['col1', 'col2'], 'tbl', **{'bool':True, 'text' : 'text', 'int':1, 'float' : 0.9324})
        
        query_body = f"SELECT {_value} FROM {self.source_db['schemaName']}.{_from}"
        check_str = lambda x: f"'{x}'" if isinstance(x, str) else x
        check_bool = lambda x: str(x).lower() if isinstance(x, bool) else str(x)
        where_list = [f"{k}={check_bool(check_str(v))}" for k, v in _where.items()]
        query_body = query_body + " where " + " and ".join(where_list)+';' if where_list else query_body+';'
        # print('query_body', query_body)

        result = self.cc.query_db(query_body)

        return None if len(result) == 0 else result[0][_value]

    def create(self, row_dict):
        print('1. row_dict\n', row_dict, '\n')
        print('2. include_keys\n', self.include_keys[self.table_name], '\n')

        dict1 = {}
        for key in self.include_keys[self.table_name]:
            ### step.4 Source 테이블에서 가져온 정보를 알맞게 변환
            if key == 'blockStorageSnapshotInstanceNo' or key =='snapshotTypeCode':
                value = None
            elif key == 'targetVpcName':
                value = self.get_value('vpcname', 'vpc', **{'id' : row_dict['targetvpcid']})
                print(value)
            elif key == 'loginKeyName':
                value = self.get_value('keyname', 'loginkey', **{'id' : row_dict['loginkeyid']})
            elif key[-4:] == 'Name':    # 테스트 환경에서 Naver Cloud가 하나뿐이므로, 중복이름인경우 생성이 불가하기에 예외처리
                # RouteTable, PlacementGroup
                value = row_dict[key.lower()] + '-dr'
            elif self.table_name == 'launchconfiguration' and key == 'serverProductCode':
                value = self.get_value('productcode', 'product', **{'id' : row_dict['serverproductid']})
            elif key == 'serverImageProductCode':   # 서버 인스턴스 생성시 serverImageProductCode 혹은 memberServerImageInstanceNo 중 하나만 선택하여 생성함
                value = row_dict['serverimageproductcode']
                if value == None:   # None일 때 serverImageProductCode를 가지고 생성한 것이 아니기 때문에 키를 삭제하고 멤버서버로 설정
                    key = 'memberServerImageInstanceNo'
            elif key == 'serverProductCode':
                value = self.get_value('productcode', 'product', **{'id' : row_dict['serverproductcodeid']})
                if value == None:   # None일 때 serverImageProductCode를 가지고 생성한 것이 아니기 때문에 키를 삭제하고 멤버서버로 설정
                    key = 'memberServerImageInstanceNo'
            elif key == 'memberServerImageInstanceNo':#서버 인스턴스 생성시 serverImageProductCode 혹은 memberServerImageInstanceNo 중 하나만 선택하여 생성함
                value = row_dict['memberserverimageinstanceno']
            elif self.table_name == 'memberserverimageinstance' and key == 'serverInstanceNo':
                value = self.get_value('originalserverinstanceid', 'memberserverimageinstance', **{'id': row_dict['originalserverinstanceid']})
            # elif key == 'vpcNo':
            #     try:
            #         value = self.get_value('vpcno', 'vpc', **{'id' : row_dict['vpcid']})
            #     except: # networkinterface 부분
            #         _value_temp = self.get_value('vpcid', 'subnet', **{'id' : row_dict['subnetid']})
            #         value = self.get_value('vpcno', 'vpc', **{'id' : _value_temp})
            elif key in ['secondaryIpList.N', 'secondaryIpCount']:
                value = None
            elif key in ['subnetNo', 'serverInstanceNo']:
                value = self.get_value('subnetno', 'subnet', **{'id' : row_dict['subnetid']})
            elif key == 'zoneCode':
                value = self.get_value('zonecode', 'zone', **{'id' : row_dict['id']})
            elif key == 'blockStorageVolumeTypeCode':
                pass
            elif key == 'blockStorageSize':
                value = row_dict['blockstoragesize']
                value = round(value/(1024**3))
            elif key == 'originalBlockStorageInstanceNo':
                value = row_dict['blockstoragesnapshotinstanceno']
            elif key == 'sourceVpcNo':
                value = self.get_value('vpcno', 'vpc', **{'id' : row_dict['sourcevpcid']})
            elif key == 'targetVpcNo':
                value = self.get_value('vpcno', 'vpc', **{'id' : row_dict['targetvpcid']})
            elif key == 'loadBalancerTypeCode':
                value = row_dict['loadbalancertype']  # 이 예제에서 db의 정보가 Code가 아닌 값으로 저장되어있어 예외처리
            elif key in ['loadBalancerNetworkTypeCode', 'throughputTypeCode']:
                value = row_dict[key[:-4].lower()].upper() # 이 예제에서 db의 정보가 Code가 아닌 값으로 저장되어있어 예외처리
                print('value', value)
            elif key in ['supportedSubnetTypeCode', 'placementGroupTypeCode', 'blockStorageDiskDetailTypeCode', 'healthCheckHttpMethodTypeCode', 
                         'healthCheckProtocolTypeCode', 'targetGroupProtocolTypeCode', 'targetTypeCode', 'accessControlGroupStatusCode', 'osTypeCode']:
                value = row_dict[key[:-4].lower()]
            elif key == 'loadBalancerInstanceNo':
                value = self.get_value('loadbalancerinstanceno', 'loadbalancerinstance', **{'id' : row_dict['loadbalancerinstanceid']})
            elif key == 'networkInterfaceNoList':#양식이 조금 달라서 .N 에 넣지 않았음
                # 만들어야하는 키 목록 1. networkInterfaceOrder, 2. accessControlGroupNoList
                # networkInterfaceList.N.networkInterfaceNo
                cnt = 0
                for nic in row_dict['networkinterfacenolist']:
                    #네트워크인터페이스가 할당중이라면 실패함, 할당할 네트워크인터페이스가 서버에 붙어있지 않은 상태에서만 networkInterfaceNo 부여가 가능
                    #k1 = f'networkInterfaceList.{cnt+1}.networkInterfaceNo'
                    #v1 = f'{nic}'
                    #dict1.update({k1: v1})
                    k2 = f'networkInterfaceList.{cnt+1}.networkInterfaceOrder'
                    v2 = f'{cnt}'
                    dict1.update({k2: v2})
                    acg_cnt = 0
                    acg_list = self.get_value('accesscontrolgroupnolist', 'networkinterface', **{'networkinterfaceno' : nic})
                    for acg in acg_list:
                        k3 = f'networkInterfaceList.{cnt+1}.accessControlGroupNoList.{acg_cnt+1}'
                        v3 = f'{acg}'
                        dict1.update({k3: v3})
                    cnt += 1
                continue

            elif key == 'accessControlGroupNo' :
                value = self.get_value('accesscontrolgroupno', 'accesscontrolgroup', **{'id' : row_dict['accesscontrolgroupid']})
            elif '.N' in key:   # DB 컬럼명 중 'List'로 끝나는 컬럼 중점적으로 자료형 사전 통일 필요 from readVPC2InsertDB
                # networkInterfaceList
                # 만들어야하는 키 목록 1. networkInterfaceOrder, 2. accessControlGroupNoList
                _temp_key = key.split('.N')
                _main_key, _sub_key = _temp_key[0], _temp_key[1] if _temp_key[1] else None
                #obj = eval(row_dict[_main_key.lower()])
                if _main_key == 'loadBalancerListenerList' and _sub_key == '.targetGroupNo':
                    cnt = 0
                    query = f"SELECT * FROM {self.source_db['schemaName']}.targetgroup WHERE loadbalancerinstanceno = '{row_dict['loadbalancerinstanceno']}'"
                    self.cur.execute(query)
                    results1 = self.cur.fetchall()
                    print("result1 :",results1)
                    query = f"SELECT * FROM {self.source_db['schemaName']}.targetgroup WHERE loadbalancerinstanceno = '' "
                    self.cur.execute(query)
                    results2 = self.cur.fetchall() #알고리즘 1번
                    print("results2 :",results2)
                    if len(results1) == len(results2):
                        for index in range(len(results1)):
                            i = results1[index]
                            j = results2[index]

                            # i와 j의 특정 필드 비교
                            if all(i[k] == j[k] for k in [3, 5, 6, 8, 9, 10, 14, 15, 16, 17, 18, 19, 20]):
                                key = f'loadBalancerListenerList.{cnt+1}.targetGroupNo'
                                value = j[1]
                                dict1.update({key: value})
                                print("key, value :", key, value)
                                cnt += 1
                            else :
                                pass
                    continue
                elif _main_key == 'subnetNoList' and _sub_key == None :
                    _value = row_dict[_main_key.lower()]
                    for index, value in enumerate(_value, start=1):
                        key = f"subnetNoList.{index}"
                elif _main_key == 'loadBalancerListenerList' and _sub_key == '.protocolTypeCode' :
                    _value = self.get_value('protocoltype', 'loadbalanerlistener', **{'loadbalancerinstanceid' : row_dict['id']})
                    if _value == 'UDP':
                        pass
                    else :
                        value = _value
                elif _main_key == 'loadBalancerSubnetList' and _sub_key == '.publicIpInstanceNo' :
                    _value_ = row_dict['loadbalancersubnetlist']
                    _value = [item["publicIpInstanceNo"] for item in _value_ if "publicIpInstanceNo" in item]
                    value = _value[0]
                else :
                    continue
            elif key == 'loadBalancerNetworkTypeCode' :
                value = row_dict['loadbalancernetworktype']
            elif key == 'accessControlGroupNoList':
                key = "accessControlGroupNoList.1"
                value = ''.join(row_dict['accesscontrolgroupnolist'])
                print(key, value)
            elif key == 'protocolTypeCode':
                value = row_dict['protocoltype']
            elif key == 'targetGroupNo' and self.table_name == 'loadbalancerlistener' :
                _value = self.get_value('vpcid', 'loadbalancerinstance', **{'id' : row_dict['loadbalancerinstanceid']})
                value = self.get_value('targetgroupno', 'targetgroup', **{'vpcid' : _value})
            elif key == 'port':
                value = 8080
            else:
                value = row_dict[key.lower()]

            dict1.update({key : value})
        
        dict1 = {k: v for k, v in dict1.items() if v is not None}
        print('3. body\n', self.pretty_dict(dict1), '\n')
        result = self.cc.request_api(self.api_url, self.sub_url, **dict1)
        print('4. request result\n', self.pretty_dict(result), '\n')

        if 'responseError' in result:
            raise Exception("[ERR] " + str(result))
        else:
            return dict1
        
    # AUTHOR: 차동현 / cdh@cbnu.ac.kr
    # DATE: 2024-01-29
    # DESCRIPTION: 무료 자원에 대하여 모든 자원 생성 및 특정 자원에 대하여 생성
    # TODO: 전체 자원에 대하여 생성 
        
    def run(self):
        ### for this in self.nc.keys():
        this = 'all' ### step.1 본인 Table을 기입, all로 설정시 전체 자원 생성
        if this == 'all':
            for this in naverCloud.include_keys():
                try:
                    self.set_url(this, "create")
                except KeyError:
                    pass    # continue
                # Unit test
                if this == 'loadbalancerlistener':
                    tmp_query = f"SELECT * FROM {self.source_db['schemaName']}.loadbalancerinstance WHERE loadbalancerlistenernolist = '[]';"
                    self.cur.execute(tmp_query)
                    resultslllr = self.cur.fetchall()
                    print("len-------------",len(resultslllr))
                    for i in range(len(resultslllr)):
                            row = resultslllr[i]
                            self.create(row)
                            print("row is : ", row)
                            self.set_url(this, "read")
                            print('5. api result\n', self.pretty_dict(self.read_db()), '\n')
                            i+=1
                else:
                    row = self.get_table()[0]
                    for key in row.keys():
                        try:
                            if this != 'vpc':
                                if key == 'vpcno':
                                    row[key] =  tmp_vpcno
                                elif key == 'accesscontrolgroupno':
                                    row[key] =  tmp_acgno
                                elif key ==  'memberserverimageinstanceno':
                                    row[key] =  tmp_msiino
                                elif key == 'launchconfigurationno':
                                    row[key] =  tmp_lcno
                                elif key == 'subnetno':
                                    row[key] =  tmp_subnetno
                        except:
                            pass
                    print("@@@@@@@@@@ row is : ", row)
                    print('row is self.create(row) : ', row)
                    try:
                        self.create(row)
                        self.set_url(this, "read")
                    except:
                        pass
                    print('5. api result\n', self.pretty_dict(self.read_db()), '\n')
                    if this == 'vpc':
                        tmp_vpcno = json.loads(self.pretty_dict(self.read_db()))['getVpcListResponse']['vpcList'][0]['vpcNo'] 
                    elif this == 'accesscontrolgroup':
                        tmp_acgno = json.loads(self.pretty_dict(self.read_db()))['getAccessControlGroupListResponse']['accessControlGroupList'][0]['accessControlGroupNo'] 
                    elif this == 'memberserverimageinstance':
                        tmp_msiino = json.loads(self.pretty_dict(self.read_db()))['getmemberServerImageInstanceListResponse']['memberServerImageInstanceList'][0]['memberServerImageInstanceNo'] 
                    elif this == 'launchconfiguration':
                        tmp_lcno = json.loads(self.pretty_dict(self.read_db()))['getlaunchConfigurationListResponse']['launchConfigurationList'][0]['launchConfigurationNo']
                    elif this == 'subnet':
                        tmp_subnetno = json.loads(self.pretty_dict(self.read_db()))['getsubnetListResponse']['subnetList'][0]['subnetNo']
                # try:
                #     self.create(row)
                # except Exception as e:
                #     print(e)
                # finally:
                #     self.set_url(this, "read")
                #     print('5. api result\n', self.pretty_dict(self.read_db()), '\n')
                    ### step.5 터미널에 출력되는 1~5를 확인
                
                # Integration test
                # rows = self.get_table()
                # for row in rows:
                #     try:
                #         self.create(row)
                #     except Exception as e:
                #         print(e)
                #     finally:
                #         self.set_url(this, "read")
                #         print('5. api result\n', self.pretty_dict(self.read_db()), '\n')
        else:
            try:
                self.set_url(this, "create")
            except KeyError:
                pass    # continue
            # Unit test
            if this == 'loadbalancerlistener':
                tmp_query = f"SELECT * FROM {self.source_db['schemaName']}.loadbalancerinstance WHERE loadbalancerlistenernolist = '[]';"
                self.cur.execute(tmp_query)
                resultslllr = self.cur.fetchall()
                print("len-------------",len(resultslllr))
                for i in range(len(resultslllr)):
                        row = resultslllr[i]
                        self.create(row)
                        print("row is : ", row)
                        self.set_url(this, "read")
                        print('5. api result\n', self.pretty_dict(self.read_db()), '\n')
                        i+=1
            else:
                row = self.get_table()[0]
                self.create(row)
                self.set_url(this, "read")
                print('5. api result\n', self.pretty_dict(self.read_db()), '\n')
            # try:
            #     self.create(row)
            # except Exception as e:
            #     print(e)
            # finally:
            #     self.set_url(this, "read")
            #     print('5. api result\n', self.pretty_dict(self.read_db()), '\n')
                ### step.5 터미널에 출력되는 1~5를 확인
            
            # Integration test
            # rows = self.get_table()
            # for row in rows:
            #     try:
            #         self.create(row)
            #     except Exception as e:
            #         print(e)
            #     finally:
            #         self.set_url(this, "read")
            #         print('5. api result\n', self.pretty_dict(self.read_db()), '\n')            