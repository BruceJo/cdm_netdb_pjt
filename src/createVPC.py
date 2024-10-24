import connDbnApi as cda
import naverCloud
import json
import re


class Create():
    def __init__(self, source_db, target_api, cancel_flag=None):
        self.source_db = source_db
        self.cancel_flag = cancel_flag
        self.target_api = target_api
        self.nc = naverCloud.url_info()
        self.include_keys = naverCloud.include_keys()
        self.cc = cda.Connect(api=target_api, db=source_db)
        self.conn = self.cc.connect_cockroachdb()
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
        self.recovery_schema = "recovery"
        self.creatable_resources = {key: value for key, value in self.nc.items() if 'create' in value}

    def read_db(self):
        res = self.cc.request_api(self.api_url, self.sub_url)
        return res

    def is_valiable_table(self, table_name):
        return table_name.lower() in (resource.lower() for resource in self.creatable_resources)

    def pretty_dict(self, _dict: dict):
        return json.dumps(_dict, sort_keys=True, indent=4)

    def set_url(self, name, action):
        self.table_name, self.api_url, self.sub_url = naverCloud.set_url(name, action)

    def get_table(self):
        result = self.cc.query_db(f"SELECT * FROM {self.source_db['schemaName']}.{self.table_name}")
        return None if len(result) == 0 else result

    def get_value(self, _value: str, _from: str, **_where: dict):
        # usage -> self.get_value(['col1', 'col2'], 'tbl')
        # usage -> self.get_value(['col1', 'col2'], 'tbl', **{'bool':True, 'text' : 'text', 'int':1, 'float' : 0.9324})

        query_body = f"SELECT {_value} FROM {self.source_db['schemaName']}.{_from}"
        check_str = lambda x: f"'{x}'" if isinstance(x, str) else x
        check_bool = lambda x: str(x).lower() if isinstance(x, bool) else str(x)
        where_list = [f"{k}={check_bool(check_str(v))}" for k, v in _where.items()]
        query_body = query_body + " where " + " and ".join(where_list) + ';' if where_list else query_body + ';'
        print('query_body', query_body)

        result = self.cc.query_db(query_body)

        return None if len(result) == 0 else result[0][_value]

    def create(self, row_dict):
        print('1. row_dict\n', row_dict, '\n')
        print('2. include_keys\n', self.include_keys[self.table_name], '\n')

        dict1 = {}
        for key in self.include_keys[self.table_name]:
            ### step.4 Source 테이블에서 가져온 정보를 알맞게 변환
            if key == 'blockStorageSnapshotInstanceNo' or key == 'snapshotTypeCode':
                value = None
            elif key == 'subnetTypeCode':
                value = self.get_value('subnettype', 'subnet', **{'subnetno': row_dict['subnetno']})
                print("!!!!!!!", value)
            elif key == 'targetVpcName':
                value = self.get_value('vpcname', 'vpc', **{'id': row_dict['targetvpcid']})
                # print(value)
            elif key == 'loginKeyName':
                value = self.get_value('keyname', 'loginkey', **{'id': row_dict['loginkeyid']})
            elif key[-4:] == 'Name':  # 테스트 환경에서 Naver Cloud가 하나뿐이므로, 중복이름인경우 생성이 불가하기에 예외처리
                value = row_dict[key.lower()] + '-dr'
            elif self.table_name == 'launchconfiguration' and key == 'serverProductCode':
                value = self.get_value('productcode', 'product', **{'id': row_dict['serverproductid']})
            elif key == 'serverImageProductCode':  # 서버 인스턴스 생성시 serverImageProductCode 혹은 memberServerImageInstanceNo 중 하나만 선택하여 생성함
                value = row_dict['serverimageproductcode']
                if value == None:  # None일 때 serverImageProductCode를 가지고 생성한 것이 아니기 때문에 키를 삭제하고 멤버서버로 설정
                    key = 'memberServerImageInstanceNo'
            elif key == 'serverProductCode':
                value = self.get_value('productcode', 'product', **{'id': row_dict['serverproductcodeid']})
                if value == None:  # None일 때 serverImageProductCode를 가지고 생성한 것이 아니기 때문에 키를 삭제하고 멤버서버로 설정
                    key = 'memberServerImageInstanceNo'
            elif key == 'memberServerImageInstanceNo':  # 서버 인스턴스 생성시 serverImageProductCode 혹은 memberServerImageInstanceNo 중 하나만 선택하여 생성함
                value = row_dict['memberserverimageinstanceno']
            elif self.table_name == 'memberserverimageinstance' and key == 'serverInstanceNo':
                value = self.get_value('originalserverinstanceid', 'memberserverimageinstance',
                                       **{'id': row_dict['originalserverinstanceid']})
            elif key == 'vpcNo':
                try:
                    value = self.get_value('vpcno', 'vpc', **{'id': row_dict['vpcid']})
                except:  # networkinterface 부분
                    _value_temp = self.get_value('vpcid', 'subnet', **{'id': row_dict['subnetid']})
                    value = self.get_value('vpcno', 'vpc', **{'id': _value_temp})
            elif key in ['secondaryIpList.N', 'secondaryIpCount']:
                value = None
            elif key in ['subnetNo', 'serverInstanceNo']:
                if self.table_name == 'blockstorageinstance':
                    value = row_dict['serverinstanceno']
                else:
                    value = self.get_value('subnetno', 'subnet', **{'id': row_dict['subnetid']})
            elif key == 'zoneCode':
                value = self.get_value('zonecode', 'zone', **{'id': row_dict['id']})
            elif key == 'blockStorageVolumeTypeCode':
                pass
            elif key == 'blockStorageSize':
                value = row_dict['blockstoragesize']
                value = round(value / (1024 ** 3))
            elif key == 'originalBlockStorageInstanceNo':
                value = row_dict['blockstoragesnapshotinstanceno']
            elif key == 'sourceVpcNo':
                value = self.get_value('vpcno', 'vpc', **{'id': row_dict['sourcevpcid']})
            elif key == 'targetVpcNo':
                value = self.get_value('vpcno', 'vpc', **{'id': row_dict['targetvpcid']})
            elif key == 'loadBalancerTypeCode':
                value = row_dict['loadbalancertype']  # 이 예제에서 db의 정보가 Code가 아닌 값으로 저장되어있어 예외처리
            elif key in ['loadBalancerNetworkTypeCode', 'throughputTypeCode']:
                value = row_dict[key[:-4].lower()].upper()  # 이 예제에서 db의 정보가 Code가 아닌 값으로 저장되어있어 예외처리
                print('value', value)
            elif key in ['supportedSubnetTypeCode', 'placementGroupTypeCode', 'blockStorageDiskDetailTypeCode',
                         'healthCheckHttpMethodTypeCode',
                         'healthCheckProtocolTypeCode', 'targetGroupProtocolTypeCode', 'targetTypeCode',
                         'accessControlGroupStatusCode', 'osTypeCode']:
                value = row_dict[key[:-4].lower()]
            elif key == 'loadBalancerInstanceNo':
                value = self.get_value('loadbalancerinstanceno', 'loadbalancerinstance',
                                       **{'id': row_dict['loadbalancerinstanceid']})
            elif key == 'networkInterfaceNoList':  # 양식이 조금 달라서 .N 에 넣지 않았음
                # 만들어야하는 키 목록 1. networkInterfaceOrder, 2. accessControlGroupNoList
                # networkInterfaceList.N.networkInterfaceNo
                # nic_list = re.findall(r'\d+', row_dict['networkinterfacenolist'])
                # -------------------------------------------------------
                # row_dict['networkinterfacenolist']가 문자열인지 확인
                network_interface_list = row_dict.get('networkinterfacenolist')

                if isinstance(network_interface_list, str):
                    # 문자열인 경우에만 정규 표현식 처리
                    nic_list = re.findall(r'\d+', network_interface_list)
                else:
                    # 문자열이 아닌 경우 적절한 처리 (예: None 처리)
                    nic_list = []
                    print(f"Invalid type for networkinterfacenolist: {type(network_interface_list)}")
                    for i in range(len(network_interface_list)):
                        nic_list.append(str(network_interface_list[i]))
                    print(f"nic_list: {nic_list}")
# -----------------------------------------------------------
                cnt = 0
                for nic in nic_list:
                    print(f"nic: {nic}")
                    # 네트워크인터페이스가 할당중이라면 실패함, 할당할 네트워크인터페이스가 서버에 붙어있지 않은 상태에서만 networkInterfaceNo 부여가 가능
                    # k1 = f'networkInterfaceList.{cnt+1}.networkInterfaceNo'
                    # v1 = f'{nic}'
                    # dict1.update({k1: v1})
                    k2 = f'networkInterfaceList.{cnt + 1}.networkInterfaceOrder'
                    v2 = f'{cnt}'
                    dict1.update({k2: v2})
                    acg_cnt = 0
                    # acg_list = self.get_value('accesscontrolgroupnolist', 'networkinterface', **{'networkinterfaceno' : nic})
                    acg_list_str = self.get_value('accesscontrolgroupnolist', 'networkinterface',
                                                  **{'networkinterfaceno': nic})
                    if acg_list_str is not None:
                        if isinstance(network_interface_list, str):
                            acg_list = re.findall(r'\d+', acg_list_str)  # 문자열에서 숫자 값 추출
                            for acg in acg_list:
                                k3 = f'networkInterfaceList.{cnt + 1}.accessControlGroupNoList.{acg_cnt + 1}'
                                v3 = f'{acg}'
                                dict1.update({k3: v3})
                        else:
                            acg_list = []
                            acg_list = acg_list_str
                            for acg in acg_list:
                                k3 = f'networkInterfaceList.{cnt + 1}.accessControlGroupNoList.{acg_cnt + 1}'
                                v3 = f'{acg}'
                                dict1.update({k3: v3})
                    cnt += 1
                continue

            elif key == 'accessControlGroupNo':
                value = self.get_value('accesscontrolgroupno', 'accesscontrolgroup',
                                       **{'id': row_dict['accesscontrolgroupid']})
            elif '.N' in key:  # DB 컬럼명 중 'List'로 끝나는 컬럼 중점적으로 자료형 사전 통일 필요 from readVPC2InsertDB
                # networkInterfaceList
                # 만들어야하는 키 목록 1. networkInterfaceOrder, 2. accessControlGroupNoList
                _temp_key = key.split('.N')
                _main_key, _sub_key = _temp_key[0], _temp_key[1] if _temp_key[1] else None
                # obj = eval(row_dict[_main_key.lower()])
                if _main_key == 'loadBalancerListenerList' and _sub_key == '.targetGroupNo':
                    cnt = 0
                    query = f"SELECT * FROM {self.source_db['schemaName']}.targetgroup WHERE loadbalancerinstanceno = '{row_dict['loadbalancerinstanceno']}'"
                    self.cur.execute(query)
                    results1 = self.cur.fetchall()
                    print("result1 :", results1)
                    query = f"SELECT * FROM {self.source_db['schemaName']}.targetgroup WHERE loadbalancerinstanceno = '' "
                    self.cur.execute(query)
                    results2 = self.cur.fetchall()  # 알고리즘 1번
                    print("results2 :", results2)
                    if len(results1) == len(results2):
                        for index in range(len(results1)):
                            i = results1[index]
                            j = results2[index]

                            # i와 j의 특정 필드 비교
                            if all(i[k] == j[k] for k in [3, 5, 6, 8, 9, 10, 14, 15, 16, 17, 18, 19, 20]):
                                key = f'loadBalancerListenerList.{cnt + 1}.targetGroupNo'
                                value = j[1]
                                dict1.update({key: value})
                                print("key, value :", key, value)
                                cnt += 1
                            else:
                                pass
                    continue
                elif _main_key == 'subnetNoList' and _sub_key == None:
                    _value = row_dict[_main_key.lower()]
                    for index, value in enumerate(_value, start=1):
                        key = f"subnetNoList.{index}"
                elif _main_key == 'loadBalancerListenerList' and _sub_key == '.protocolTypeCode':
                    _value = self.get_value('protocoltype', 'loadbalanerlistener',
                                            **{'loadbalancerinstanceid': row_dict['id']})
                    if _value == 'UDP':
                        pass
                    else:
                        value = _value
                elif _main_key == 'loadBalancerSubnetList' and _sub_key == '.publicIpInstanceNo':
                    _value_ = row_dict['loadbalancersubnetlist']
                    _value = [item["publicIpInstanceNo"] for item in _value_ if "publicIpInstanceNo" in item]
                    value = _value[0]
                else:
                    continue
            elif key == 'loadBalancerNetworkTypeCode':
                value = row_dict['loadbalancernetworktype']
            elif key == 'accessControlGroupNoList':
                key = "accessControlGroupNoList.1"
                value = ''.join(row_dict['accesscontrolgroupnolist'])
                print(key, value)
            elif key == 'protocolTypeCode':
                value = row_dict['protocoltype']
            elif key == 'targetGroupNo' and self.table_name == 'loadbalancerlistener':
                _value = self.get_value('vpcid', 'loadbalancerinstance', **{'id': row_dict['loadbalancerinstanceid']})
                value = self.get_value('targetgroupno', 'targetgroup', **{'vpcid': _value})
            elif key == 'port':
                value = 8080
            else:
                value = row_dict[key.lower()]

            dict1.update({key: value})

        dict1 = {k: v for k, v in dict1.items() if v is not None}
        print('3. body\n', self.pretty_dict(dict1), '\n')
        result = self.cc.request_api(self.api_url, self.sub_url, **dict1)
        print('4. request result\n', self.pretty_dict(result), '\n')

        if 'responseError' in result:
            raise Exception("[ERR] " + str(result))
        else:
            return dict1

    def run(self, resource_name, filtering_info=None, recoveryplanid=None):
        print(f"### create resource name >> {resource_name}")
        
        recovery_list = []
        sent_flag = False

        if resource_name == 'recoveryplan':
            order_table = naverCloud.get_ordered_table_list()

            # completeflag가 false인 모든 데이터를 가져옴
            get_recoveryplans_query = "SELECT * FROM recovery.recoveryplan WHERE completeflag=false;"
            #"SELECT * FROM recovery.recoveryplan WHERE completeflag=false AND planid={job1} or {job2};"
            self.cur.execute(get_recoveryplans_query)
            current_recoveryplans = self.cur.fetchall()

            # recoveryplan 데이터가 없을 경우 예외 처리
            if not current_recoveryplans:
                raise Exception("[ERR] No recoveryplan data found")

            # 데이터를 정렬 (order_table의 순서에 맞게 정렬)
            sorted_recovery_plans = sorted(
                current_recoveryplans, key=lambda x: order_table.get(x[2], float('inf'))
            )

            # 정렬된 데이터를 처리 (처리 로직을 여기에서 수행)
            for recovery_plan in sorted_recovery_plans:
                recoveryplanid = recovery_plan[0]  #recoveryplanid 설정
                print(f"Processing recoveryplan id: {recoveryplanid}")

            # completeflag를 true로 업데이트 (정렬된 후 모든 recoveryplan 처리 완료 후에)
            for recovery_plan in sorted_recovery_plans:
                recoveryplanid = recovery_plan[0]
                update_completeflag_query = f"""
                UPDATE recovery.recoveryplan 
                SET completeflag=true 
                WHERE completeflag=false 
                AND id={recoveryplanid};
                """
                self.cur.execute(update_completeflag_query)

            # recovery_list에 마지막으로 처리된 resource_name 추가
            recovery_list.append(resource_name)

        ########################################################

        for this in recovery_list:
            if self.cancel_flag and self.cancel_flag.is_set():
                print(f"Recovery process for {resource_name} cancelled during {this} creation.")
                return 'Recovery cancelled'
            print(f"create resource => {this}")
            if 1 == 1:  # 조건을 변경하려면 여기에 넣으세요
                print("process ...")
                
                # SQL 쿼리, 파라미터 바인딩 사용
                query_body = f"SELECT resourcetype FROM recovery.recoveryplan WHERE id = {recoveryplanid};"
                self.cur.execute(query_body)

                resourcetype_in_db = self.cur.fetchall()

                # URL 설정
                self.set_url(resourcetype_in_db[0][0], "create")
                # 테이블 데이터 가져오기
                row = self.get_table()

                # filtering_info 적용
                if filtering_info is not None:
                    for r in row:
                        for key, value in filtering_info.items():
                            if key in r:
                                r[key] = value

                for r in row:                    
                    if self.cancel_flag and self.cancel_flag.is_set():
                        print(f"Recovery process for {resource_name} cancelled during {resourcetype_in_db} creation.")
                        return 'Recovery cancelled'
                    if r == 'serverinstance': # serverinstance의 하위 자원 복제
                        include_rscs = ["vpc", "networkacl", "subnet", "networkinterface"]
                        for rsc in include_rscs:
                            self.set_url(rsc, "create")
                            row_tmp = self.get_table()[0]
                            self.create(row_tmp)
                    try:
                        self.create(r)
                    except Exception as e:
                        print(f"[ERR] "+ e)
                        continue
                    if resource_name == 'recoveryplan':
                        # sourcekey 가져오기
                        tmp_res_query = "SELECT sourcekey FROM recovery.recoveryplan WHERE id = %s;"
                        self.cur.execute(tmp_res_query, (recoveryplanid,))
                        tmp_res = list(self.cur.fetchall())[0][0]

                        # URL 설정
                        self.table_name = resourcetype_in_db
                        print("resourcetype_in_db", resourcetype_in_db)
                        tmp_res_2 = resourcetype_in_db
                        self.set_url(tmp_res_2[0], "read")

                        # API 결과 가져오기
                        api_res = self.pretty_dict(self.read_db())
                        print('5. api result\n', api_res, '\n')

                        if sent_flag == False:
                            print('5.1. Send information into recovery result table.')

                            # recoveryplan 업데이트 및 결과 테이블에 삽입
                            update_recoveryplan_query = "UPDATE recovery.recoveryplan SET completeflag=true WHERE sourcekey=%s;"
                            self.cur.execute(update_recoveryplan_query, (tmp_res,))

                            # 요청 ID와 자원 유형 가져오기
                            select_query = "SELECT requestid, resourcetype FROM recovery.recoveryplan WHERE sourcekey=%s;"
                            self.cur.execute(select_query, (tmp_res,))
                            x = list(self.cur.fetchall())

                            # API 응답에서 특정 값을 추출
                            loaded_res = json.loads(api_res)
                            if tmp_res_2[0] == 'vpc':
                                this_no = loaded_res['getVpcListResponse']['vpcList'][0]['vpcNo']
                                this_code = loaded_res['getVpcListResponse']['vpcList'][0]['vpcStatus']['code']
                                y = (this_no, this_code)
                            elif tmp_res_2[0] == 'serverinstance' or tmp_res_2[0] == 'serverInstance' or tmp_res_2[0] == 'Serverinstance' or tmp_res_2[0] == 'ServerInstance':
                                before_this = 'serverInstance'
                                this_no = loaded_res['getServerInstanceListResponse']['serverInstanceList'][0][
                                    'serverInstanceNo']
                                this_code = loaded_res['getServerInstanceListResponse']['serverInstanceList'][0][
                                    'serverInstanceStatus']['code']
                                y = (this_no, this_code)
                            elif tmp_res_2[0] == 'subnet':
                                before_this = tmp_res_2[0]
                                this_no = loaded_res[f'getSubnetListResponse'][f'subnetList'][0][
                                    f'{before_this}No']
                                this_code = loaded_res[f'getSubnetListResponse'][f'subnetList'][0][
                                    f'{before_this}Status']['code']
                                y = (this_no, this_code)
                            elif tmp_res_2[0] == 'networkacl':
                                before_this = tmp_res_2[0]
                                this_no = loaded_res[f'getNetworkAclListResponse'][f'networkAclList'][0][
                                    f'networkAclNo']
                                this_code = loaded_res[f'getNetworkAclListResponse'][f'networkAclList'][0][
                                    f'networkAclStatus']['code']
                                y = (this_no, this_code)
                            else:
                                try:
                                    this_no = loaded_res['getServerInstanceListResponse']['serverInstanceList'][0][
                                    'serverInstanceNo']
                                    this_code = loaded_res['getServerInstanceListResponse']['serverInstanceList'][0][
                                    'serverInstanceStatus']['code']
                                    y = (this_no, this_code)
                                except:
                                    y = ('0', 'err')
                            # 결과 테이블에 데이터 삽입
                            import datetime
                            current_timestamp = datetime.datetime.now()

                            insert_query = """
                            INSERT INTO recovery.recoveryresults (requestid, resourcetype, targetkey, sourcekey, timestamp, status, detail) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            """
                            self.cur.execute(insert_query, (x[0][0], x[0][1], y[0], tmp_res, current_timestamp, y[1], api_res))
                            self.conn.commit()
                            sent_flag = True


                        # DB 연결 닫기
                self.conn.close()
