# CDM_NETDB_PJT

## 작업내역
| 테이블 이름 |	담당자 |	데이터 입력 |	생성 |	삭제 |	수정 |	비고 |
|------|------|------|------|------|------|------|
| protocoltype                        | 상우 | <span style='color: red;'>**△**</span>	| -	| -	| -	| <span style='color: red;'>상수처럼 취급, </span>CUD 불가                                                                   |
| accesscontrolgroup                  | 상우 | <span style='color: blue;'>**O**</span>	| O	| O	| -	|                                                                              |
| initscript                          | 상우 | <span style='color: blue;'>**O**</span>	| O	| O	| -	| C: initScriptContent는 필수이나 공백일 수 있음                                |
| accesscontrolgrouprule              | 상우 | <span style='color: blue;'>**O**</span>	| O	| O	| -	| D: removeAccessControlGroupInboundRule에서 <br> 1) ipBlock 또는 accessControlGroupSequence가 필수 <br> 2) portRange는 Doc.상 필수는 아니나, 실제론 필수임    |
| activitylog                         | 우동 | <span style='color: blue;'>**O**</span>	| -	| -	| -	| CUD 불가능. Scaling Action Log 조회만 가능.                                               |
| networkacl                          | 우동 | <span style='color: blue;'>**O**</span>	| O	| O	| -	| 수정 불가능                                                                               |
| subnet                              | 우동 | <span style='color: blue;'>**O**</span>	| O	| O	| -	| 수정 불가능                                                                               |
| vpc                                 | 우동 | <span style='color: blue;'>**O**</span>	| O	| O	| -	| 수정 불가능                                                                               |
| autoscalinggroup                    | 우동 | <span style='color: blue;'>**O**</span>	| O	| O	| O	|                                                                                          |
| networkaclrule                      | 우동 | <span style='color: blue;'>**O**</span>	| O	| O	| -	|                                                                                          |
| natgatewayinstance                  | 우동 | <span style='color: blue;'>**O**</span>	| O	| O	| -	|                                                                                          |
| networkacldenyallowgroup            | 우동 | <span style='color: blue;'>**O**</span>	| O	| O	| 	|                                                                                          |
| scalingpolicy                       | 우동 | <span style='color: blue;'>**O**</span>	| O	| O	| O	| <span style='color: red;'>//minadjustmentstep가 api에 포함되지 않음</span>                                             |
| scheduledupdategroupaction          | 우동 | <span style='color: blue;'>**△**</span>	| △	| △	| △	| 코드 구현 완료했으나 데이터 형식 입력에서 인증 문제 발생                                  |
| region                              | 윤아 | <span style='color: red;'>**O**</span>	| -	| -	| -	| <span style='color: red;'>상수처럼 취급</span>                                              |
| zone                                | 윤아 | <span style='color: red;'>**O**</span>	| -	| -	| -	| <span style='color: red;'>상수처럼 취급</span>                                              |
| blockstorageinstance                | 윤아 | <span style='color: blue;'>**O**</span>	| O	| O	| O	|                                                                                              |
| blockstoragesnapshotinstance        | 윤아 | <span style='color: blue;'>**O**</span>	| O	| O	| O	|                                                                                              |
| networkinterface                    | 윤아 | <span style='color: blue;'>**O**</span>	| O	| O	| O	| assignSencondaryIps, unassignSencondaryIps <- privateip발급받아서 시도해봐야함.                |
| publicipinstance                    | 윤아 | <span style='color: blue;'>**O**</span>	| O	| O	| O	|                                                                                              |
| vpcpeeringinstance                  | 윤아 | <span style='color: blue;'>**O**</span>	| O	| O	| O	| acceptOrRejectVpcPeering <- 확인필요                                                          |
| loadbalancerrule                    | 은미 | O	| -	| -	| -	| CUD 불가                                                                                      |
| loadbalancerruleaction              | 은미 | O	| -	| -	| -	| CUD 불가                                                                                      |
| loadbalancerrulecondition           | 은미 | O	| -	| -	| -	| CUD 불가                                                                                      |
| loadbalancersubnet                  | 은미 | O	| -	| -	| -	| CUD 불가                                                                                      |
| loadbalancerinstance                | 은미 | O	| O	| O	| O	| U: setLoadBalancerInstanceSubnet에서 Subnet이 하나뿐이기에 수정할 수 없음 <- 생성 후 수정 필요 <br> D: ""Not a load balancer in the busy state."" ErrMSG와 함께 실패할 수 있음 <br> D: 또한 바로 지워지지 않으며 수 초 이후 제거됨"    |
| loadbalancerlistener                | 은미 | O	| O	| O	| O	|                                                                                               |
| adjustmenttype                      | 중권 | <span style='color: blue;'>**O**</span>	| -	| -	| -	| CUD 불가                                                                                  |
| inautoscalinggroupserverinstance    | 중권 | <span style='color: blue;'>**O**</span>	| -	| -	| -	| CHANG/PRCNT/EXACT 고정                                                                    |
| launchconfiguration                 | 중권 | <span style='color: blue;'>**O**</span>	| O	| O	| -	|                                                                                           |
| placementgroup                      | 중권 | <span style='color: blue;'>**O**</span>	| O	| O	| -	|                                                                                           |
| routetable                          | 중권 | <span style='color: blue;'>**O**</span>	| O	| O	| O	|                                                                                           |
| route                               | 중권 | <span style='color: blue;'>**O**</span>	| X	| X	| -	| C: targetNo는 필수이나 공백일 수 있음 <br> D: Create 이후 수행 예정                          |
| product                             | 현병 | <span style='color: blue;'>**O**</span>	| -	| -	| -	|                                                                                           |
| MemberServerImage                   | 현병 | <span style='color: red;'>**O**</span>	| -	| -	| -	| <span style='color: red;'>사용하지 않음</span>                |
| loginkey                            | 현병 | <span style='color: blue;'>**O**</span>	| O	| O	| 	|                                                                                           |
| serverinstance                      | 현병 | <span style='color: blue;'>**O**</span>	| 	| 	| 	|                                                                                           |
| MemberServerImageInstance           | 현병 | <span style='color: blue;'>**O**</span>	| O	| O	| 	|                                                                                           |

## 디렉토리 구조
```
./
|-- conf
|   `-- app.conf
|-- schema
|   `--naverCloudSchema.sql
|-- src
|   |-- connCockroachDB.py
|   |-- createDB.py
|   |-- createVPC.py
|   |-- deleteVPC.py
|   |-- getConfig.py
|   |-- main.py
|   |-- naverCloud.py
|   |-- readVPC2InsertDB.py
|   `-- updateVPC.py
`-- README.md
```

Many thanks, Jo.