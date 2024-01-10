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
            if key[-4:] == 'Name':      # 테스트 환경에서 Naver Cloud가 하나뿐이므로, 중복이름인경우 생성이 불가하기에 예외처리
                value = row_dict[key.lower()] + '-ar' 
            elif key == 'vpcNo' :
                if key.lower() in row_dict :
                    value = row_dict['vpcno']
                elif 'vpcid' in row_dict :
                    value = self.get_value('vpcno', 'vpc', **{'id' : row_dict['vpcid']})
                else :
                    value = self.get_value('vpcno', 'accesscontrolgroup', **{'id' : row_dict['accesscontrolgroupid']})
                print(value)
            elif key == 'supportedSubnetTypeCode':  # 나중에 한번에 묶어 처리 'Code'
                value = row_dict['supportedsubnettype']
            elif key == 'zoneCode':
                value = self.get_value('zonecode', 'zone', **{'id' : row_dict['zoneid']})
            elif key == 'blockStorageDiskDetailTypeCode':
                value = row_dict['blockstoragediskdetailtype']
            elif key == 'blockStorageVolumeTypeCode':
                pass
            elif key == 'blockStorageSnapshotInstanceNo':
                value = None
            # 나중에 한번에 묶어 처리 'Code'
            elif key == 'loadBalancerTypeCode':
                value = 'APPLICATION'   # 이 예제에서 db의 정보가 Code가 아닌 값으로 저장되어있어 예외처리
            elif key in ['loadBalancerNetworkTypeCode', 'throughputTypeCode','osTypeCode']:
                value = row_dict[key[:-4].lower()].upper() # 이 예제에서 db의 정보가 Code가 아닌 값으로 저장되어있어 예외처리
                print('value', value)
            elif key in ['supportedSubnetTypeCode', 'loadBalancerTypeCode', 'loadBalancerNetworkTypeCode', 'throughputTypeCode']:
                value = row_dict[key[:-4].lower()]
            elif key == 'accessControlGroupStatusCode':
                value = row_dict['accesscontrolgroupstatus']
                
            # elif key =='accessControlGroupNo' :
            #     value = '39168'
            elif key == 'accessControlGroupNo' :
                value = self.get_value('accesscontrolgroupno', 'accesscontrolgroup', **{'id' : row_dict['accesscontrolgroupid']})
                
            elif key == 'osTypeCode':
                value = row_dict['ostype']
                
            elif key == 'accessControlGroupDescription':
                value = row_dict['accesscontrolgroupdescription']
            
            elif key == 'initScriptDescription':
                value = row_dict['initscriptdescription']
            
            elif '.N' in key:   # DB 컬럼명 중 'List'로 끝나는 컬럼 중점적으로 자료형 사전 통일 필요 from readVPC2InsertDB
                _temp_key = key.split('.N')
                _main_key, _sub_key = _temp_key[0], _temp_key[1][1:] if _temp_key[1] else None
                print(_main_key," ",_sub_key)
                # obj = eval(row_dict[_main_key.lower()])
                
                if _sub_key:
                    if _sub_key == "protocolTypeCode":
                        key = 'accessControlGroupRuleList.1.protocolTypeCode'
                        value = self.get_value('code', 'protocoltype', **{'id' : row_dict['protocoltypeid']})
                    if _sub_key == "portRange" and (row_dict['protocoltypeid'] == 2 or 4):
                        key = 'accessControlGroupRuleList.1.portRange'
                        value = row_dict['portrange']
                    if _sub_key == "ipBlock":
                        key = 'accessControlGroupRuleList.1.ipBlock'
                        value = row_dict['ipblock']
                    if _sub_key == "accessControlGroupRuleDescription":
                        key = 'accessControlGroupRuleList.1.accesscontrolgroupruledescription'
                        value = row_dict['accesscontrolgroupruledescription']
                else:
                    continue
            
            else:
                value = row_dict[key.lower()]

            dict1.update({key : value})
        print(dict1)
        dict1 = {k: v for k, v in dict1.items() if v is not None}
        print('3. body\n', self.pretty_dict(dict1), '\n')
        result = self.cc.request_api(self.api_url, self.sub_url, **dict1)
        print('4. request result\n', self.pretty_dict(result), '\n')

        if 'responseError' in result:
            raise Exception("[ERR] " + str(result))
        else:
            return dict1

    def run(self):
        ### for this in self.nc.keys():
        #this = 'accesscontrolgroup' ### step.1 본인 Table을 기입
        this = 'accesscontrolgrouprule'
        # this = 'initscript'
        
        
        try:  #이 부분은 create의 value가 한가지 일때
            self.set_url(this, "create")
        except KeyError:
            pass    # continue


        # Unit test
        
        row = self.get_table()[0]
        print("row", row)
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
        #     ## step.5 터미널에 출력되는 1~5를 확인
        
        # # Integration test
        # rows = self.get_table()
        # for row in rows:
        #     try:
        #         self.create(row)
        #     except Exception as e:
        #         print(e)
        #     finally:
        #         self.set_url(this, "read")
        #         print('5. api result\n', self.pretty_dict(self.read_db()), '\n')
