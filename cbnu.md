| code         | command                | request/response   | link                                              | comment                                                                                                                                                                                                                           |
|:-------------|:-----------------------|:-------------------|:--------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| clusterinfo  | get                    | request            | [link](#clusterinfogetrequest)                    |                                                                                                                                                                                                                                   |
| clusterinfo  | get                    | response           | [link](#clusterinfogetresponse)                   |                                                                                                                                                                                                                                   |
| clusterinfo  | sync                   | request            | [link](#clusterinfosyncrequest)                   |                                                                                                                                                                                                                                   |
| clusterinfo  | sync                   | response           | [link](#clusterinfosyncresponse)                  |                                                                                                                                                                                                                                   |
| instanceinfo | get                    | request            | [link](#instanceinfogetrequest)                   |                                                                                                                                                                                                                                   |
| instanceinfo | get                    | response           | [link](#instanceinfogetresponse)                  |                                                                                                                                                                                                                                   |
| instanceinfo | reboot                 | request            | [link](#instanceinforebootrequest)                |                                                                                                                                                                                                                                   |
| instanceinfo | reboot                 | response           | [link](#instanceinforebootresponse)               | raw 값이 xml이 아닌 json 값으로 변경 부탁드립니다.                                                                                                                                                                                                |
| resourceinfo | get                    | request            | [link](#resourceinfogetrequest)                   |                                                                                                                                                                                                                                   |
| resourceinfo | get                    | response           | [link](#resourceinfogetresponse)                  | resource 가 최상단 키값이 아닌 `"resource": { "raw": {} }` 이걸로 부탁드립니다.                                                                                                                                                                     |
| resourceinfo | set                    | request            | [link](#resourceinfosetrequest)                   | resource 가 최상단 키값이 아닌 `"resource": { "raw": {} }` 이걸로 부탁드립니다.                                                                                                                                                                     |
| resourceinfo | set                    | response           | [link](#resourceinfosetresponse)                  |                                                                                                                                                                                                                                   |
| resourceinfo | update                 | request            | [link](#resourceinfoupdaterequest)                |                                                                                                                                                                                                                                   |
| resourceinfo | update                 | response           | [link](#resourceinfoupdateresponse)               | **resourceinfo 의 update 는 없습니다.** set이 제일 먼저 들어갑니다.                                                                                                                                                                               |
| recoveryinfo | get                    | request            | [link](#recoveryinfogetrequest)                   | recoveryinfo.get.request 부분에 "data" 값이 비어있는데 여기에 plan 값이 들어가는게 맞습니다. (response에 적혀있는 부분의 값이 request로                                                                                                                              |
| recoveryinfo | get                    | response           | [link](#recoveryinfogetresponse)                  | data 는 리스트가 아닙니다. 여기엔 plan으로 감싸여져 있는게 아닌 `recovery` 데이터를 정의하여 주셔야합니다. 혹시 recovery 정의한 값이 있을까요?                                                                                                                                    |
| recoveryinfo | set                    | request            | [link](#recoveryinfosetrequest)                   | id 값은 string이 아닌 int값입니다. instance 리스트엔 uuid와 name 값이 들어갑니다.(instance 리스트의 value 는 어떻게 정의된건가요?)                                                                                                                                   |
| recoveryinfo | set                    | response           | [link](#recoveryinfosetresponse)                  |                                                                                                                                                                                                                                   |
| recoveryinfo | update                 | request            | [link](#recoveryinfoupdaterequest)                | 위에서 질문한 대로 recovery 를 정의한 값이 없을까요? raw에 다 들어 가 있는게 아닌 정의된 값이 필요합니다.                                                                                                                                                               |
| recoveryinfo | update                 | response           | [link](#recoveryinfoupdateresponse)               | 응답값이 resource 만 오는게 아니라 변경값이 적용된 전체 값이 있어야 하지않을까요?                                                                                                                                                                                |
| recoveryinfo | status                 | request            | [link](#recoveryinfostatusrequest)                | 어떤 plan의 상태값을 원하는지 plan 정보가 있어야 하지 않나요? 위에서 설명 했던 plan 정보가 들어가야합니다.                                                                                                                                                               |
| recoveryinfo | status                 | response           | [link](#recoveryinfostatusresponse)               | data 값은 리스트가 아닙니다. 응답 데이터엔 recovery 관련 리소스 상태를 나타내는 구조 정의가 필요합니다.                                                                                                                                                                 |
| recoveryinfo | delete                 | request            | [link](#recoveryinfodeleterequest)                |                                                                                                                                                                                                                                   |
| recoveryinfo | delete                 | response           | [link](#recoveryinfodeleteresponse)               |                                                                                                                                                                                                                                   |
| recoveryjob  | run                    | request            | [link](#recoveryjobrunrequest)                    | instance 가 제일 상단에서 묶어놨는데 plan이 제일 최상단에 **`job_id` 가 들어가야합니다.** (instance 가 없어야합니다.)                                                                                                                                               |
| recoveryjob  | run                    | response           | [link](#recoveryjobrunresponse)                   |                                                                                                                                                                                                                                   |
| recoveryjob  | pause                  | request            | [link](#recoveryjobpauserequest)                  |                                                                                                                                                                                                                                   |
| recoveryjob  | pause                  | response           | [link](#recoveryjobpauseresponse)                 | stop 은 구현필요                                                                                                                                                                                                                       |
| recoveryjob  | stop                   | request            | [link](#recoveryjobstoprequest)                   |                                                                                                                                                                                                                                   |
| recoveryjob  | stop                   | response           | [link](#recoveryjobstopresponse)                  |                                                                                                                                                                                                                                   |
| recoveryjob  | rollback               | request            | [link](#recoveryjobrollbackrequest)               | - instance 가 제일 상단에서 묶어놨는데 plan이 제일 최상단에 **`job_id` 가 들어가야합니다.** (instance 가 없어야합니다.)                                                                                                                                             |
| recoveryjob  | rollback               | response           | [link](#recoveryjobrollbackresponse)              |                                                                                                                                                                                                                                   |
| volumeinfo   | get                    | request            | [link](#volumeinfogetrequest)                     | instance로 리스트를 묶는게 아니라 instance_volume 으로 묶어야합니다. instance 의 uuid 가 없습니다.                                                                                                                                                         |
| volumeinfo   | get                    | response           | [link](#volumeinfogetresponse)                    | instance로 리스트를 묶는게 아니라 instance_volume 으로 묶어야합니다.                                                                                                                                                                                 |
| volumeinfo   | create                 | request            | [link](#volumeinfocreaterequest)                  | instance_volume 으로 묶고 instance 값만 있는게 아닌 volume의 type과 size 값도 넣어야합니다.                                                                                                                                                            |
| volumeinfo   | create                 | response           | [link](#volumeinfocreateresponse)                 | 응답 값에도 instance_volume 으로 묶고 serverinstanceno 값은 instance 의 uuid 에 넣고 blockstorageinstanceno 값은 volume 의 uuid 에 넣고 raw도 volume에 넣어야 하지않나요?                                                                                        |
| volumeinfo   | create_sanpshot_volume | request            | [link](#volumeinfocreate_sanpshot_volumerequest)  | instance_volume 에 감싸여진 instance 와 volume 이 있고 volume 리스트안에 volume uuid 가 있고 snapshot 리스트가 있습니다. 이곳에 snapshot의 uuid 값이 들어가야합니다. 이 api 로 생성된 볼륨을 가지고 특정 인스턴스에 attach 가 가능한지 기능점검 부탁드립니다.                                            |
| volumeinfo   | create_sanpshot_volume | response           | [link](#volumeinfocreate_sanpshot_volumeresponse) |                                                                                                                                                                                                                                   |
| volumeinfo   | delete                 | request            | [link](#volumeinfodeleterequest)                  | instance의 volume uuid 가 필요하기 때문에 instance_volume 이 감싸진 값이 필요합니다. (위에 설명한 값)                                                                                                                                                       |
| volumeinfo   | delete                 | response           | [link](#volumeinfodeleteresponse)                 |                                                                                                                                                                                                                                   |
| volumeinfo   | attach                 | request            | [link](#volumeinfoattachrequest)                  | instance로 묶는게 아닌 instance_volume 으로 묶어야 하는데 volume을 한개만 하는게 아니기때문에 volume을 리스트로 해야합니다.                                                                                                                                            |
| volumeinfo   | attach                 | response           | [link](#volumeinfoattachresponse)                 | 아래의 구조체로 표현 부탁드립니다.                                                                                                                                                                                                               |
| volumeinfo   | detach                 | request            | [link](#volumeinfodetachrequest)                  |                                                                                                                                                                                                                                   |
| volumeinfo   | detach                 | response           | [link](#volumeinfodetachresponse)                 |                                                                                                                                                                                                                                   |
| snapshotinfo | get                    | request            | [link](#snapshotinfogetrequest)                   | instance_volume 로 묶어야 합니다. 전체 정보를 요청할 땐 `"data": {}` 로 보내고 instance_volume 에 감싸여진 instance 의 uuid 만 있으면 특정 인스턴스의 volume snapshot 정보를 보내고 volume uuid 정보가 있으면 특정 인스턴스의 볼륨의 스냅샷 정보를 보내고 snapshot uuid 정보가 있으면 특정 스냅샷 정보를 보내주셔야 합니다. |
| snapshotinfo | get                    | response           | [link](#snapshotinfogetresponse)                  | 제일 상단의 값은 instance가 아니라 instance_volume 입니다.                                                                                                                                                                                      |
| snapshotinfo | create                 | request            | [link](#snapshotinfocreaterequest)                |                                                                                                                                                                                                                                   |
| snapshotinfo | create                 | response           | [link](#snapshotinfocreateresponse)               |                                                                                                                                                                                                                                   |
| snapshotinfo | delete                 | request            | [link](#snapshotinfodeleterequest)                | instance_volume 로 묶어야 합니다. instance_volume 에 감싸여진 instance 의 uuid 만 있으면 특정 인스턴스의 volume snapshot 을 삭제하고 volume uuid 정보가 있으면 특정 인스턴스의 볼륨의 스냅샷을 삭제하고 snapshot uuid 정보가 있으면 특정 스냅샷을 삭제해야 합니다.                                        |
| snapshotinfo | delete                 | response           | [link](#snapshotinfodeleteresponse)               | RecoveryInfo 인스턴스 중심으로 데이터를 구성하되, dr이 필요한 리소스들의 종속관계를 잡아서 표현해주세요. RecoveryInfo Status                                                                                                                                             |


## clusterinfo {sync, get}
### clusterinfo.get
#### clusterinfo.get.request
```
request clusterinfo.get
{
  "request": {
    "id": "528392ee-390b-4fe7-8dad-d0d741efd52e",
    "code": "clusterinfo",
    "parameter": {
      "command": "get",
      "data": {}
    }
  }
}
```
#### clusterinfo.get.response
```
response clusterinfo
{
  "response": {
    "id": "f93f6cf4-c153-4261-8b4b-f44c23e7120a",
    "code": "clusterinfo",
    "message": "success",
    "reason": "",
    "data": {
      "cluster": {
        "region": "KR-CENTRAL",
        "zone": "KR-1",
        "uuid": "5124759",
        "name": "target",
        "status": "RUN",
        "raw": {
          "vpc": {
            "id": 1,
            "regionid": 1,
            "vpcno": "5124759",
            "vpcname": "target",
            "ipv4cidrblock": "10.0.0.0/16",
            "vpcstatus": "RUN",
            "createdate": "2024-05-21T15:23:54"
          },
          "region": {
            "regionname": "KR-CENTRAL",
            "regioncode": "KR"
          },
          "zone": {
            "zonename": "KR-1",
            "zonecode": "KR-1",
            "zonedescription": "\ud3c9\ucd0c zone"
          }
        }
      }
    }
  }
}
```

### clusterinfo.sync
#### clusterinfo.sync.request
```
request clusterinfo.sync
{
  "request": {
    "id": "c354faa6-54c3-4097-99f5-a6328d46cf96",
    "code": "clusterinfo",
    "parameter": {
      "command": "sync",
      "data": {}
    }
  }
}
```
#### clusterinfo.sync.response
```
response clusterinfo
{
  "response": {
    "id": "c354faa6-54c3-4097-99f5-a6328d46cf96",
    "code": "clusterinfo",
    "message": "success",
    "reason": "",
    "data": {
      "raw": "{\n  \"success\": \"Done.\"\n}\n"
    }
  }
}
```

## instanceinfo {reboot, get}
### instanceinfo.get
#### instanceinfo.get.request
```
request instanceinfo.get
{
  "request": {
    "id": "5102b6ab-bc12-4492-8851-40397f04e66a",
    "code": "instanceinfo",
    "parameter": {
      "command": "get",
      "data": {}
    }
  }
}
```
#### instanceinfo.get.response
```
response instanceinfo
{
  "response": {
    "id": "5102b6ab-bc12-4492-8851-40397f04e66a",
    "code": "instanceinfo",
    "message": "success",
    "reason": "",
    "data": {
      "instance": [
        {
          "uuid": "3081226",
          "name": "s18fb360bc62",
          "status": "running",
          "raw": {
            "serverinstance": {
              "id": 1,
              "serverproductcodeid": 582,
              "zoneid": 1,
              "regionid": 1,
              "vpcid": 2,
              "subnetid": 2,
              "serverinstanceno": "3081226",
              "servername": "s18fb360bc62",
              "serverdescription": "source-public",
              "cpucount": 2,
              "memorysize": 4294967296,
              "platformtype": "UBD64",
              "loginkeyname": "cdmcrdb",
              "publicipinstanceno": "2475022",
              "publicip": "175.45.214.45",
              "serverinstancestatus": "RUN",
              "serverinstanceoperation": "NULL",
              "serverinstancestatusname": "running",
              "createdate": "2024-05-26T14:30:13",
              "uptime": "2024-06-11T15:48:27",
              "serverimageproductcode": "SW.VSVR.OS.LNX64.UBNTU.SVR2004.B050",
              "isprotectservertermination": false,
              "networkinterfacenolist": [
                "348071"
              ],
              "initscriptno": "",
              "serverinstancetype": "HICPU",
              "baseblockstoragedisktype": "NET",
              "baseblockstoragediskdetailtype": "SSD",
              "placementgroupno": "",
              "placementgroupname": "",
              "memberserverimageinstanceno": "3051719",
              "blockdevicepartitionlist": null
            }
          }
        }
      ]
    }
  }
}
```

### instanceinfo.reboot
#### instanceinfo.reboot.request
```
request instanceinfo.reboot
{
  "request": {
    "id": "8d883358-9f26-4a3d-971c-9d6b322f8276",
    "code": "instanceinfo",
    "parameter": {
      "command": "reboot",
      "data": {
        "instance": [
          {
            "uuid": "3081226"
          }
        ]
      }
    }
  }
}
```
#### instanceinfo.reboot.response
```
response instanceinfo
{
  "response": {
    "id": "8d883358-9f26-4a3d-971c-9d6b322f8276",
    "code": "instanceinfo",
    "message": "success",
    "reason": "",
    "data": {
      "raw": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<rebootServerInstancesResponse>\n  <requestId>db3554e2-b268-4a5f-a72c-f71383203588</requestId>\n  <returnCode>0</returnCode>\n  <returnMessage>success</returnMessage>\n  <totalRows>1</totalRows>\n  <serverInstanceList>\n    <serverInstance>\n      <serverInstanceNo>3081226</serverInstanceNo>\n      <serverName>s18fb360bc62</serverName>\n      <serverDescription>source-public</serverDescription>\n      <cpuCount>2</cpuCount>\n      <memorySize>4294967296</memorySize>\n      <platformType>\n        <code>UBD64</code>\n        <codeName>Ubuntu Desktop 64 Bit</codeName>\n      </platformType>\n      <loginKeyName>cdmcrdb</loginKeyName>\n      <publicIpInstanceNo>2475022</publicIpInstanceNo>\n      <publicIp>175.45.214.45</publicIp>\n      <serverInstanceStatus>\n        <code>RUN</code>\n        <codeName>Server RUN State</codeName>\n      </serverInstanceStatus>\n      <serverInstanceOperation>\n        <code>RESTA</code>\n        <codeName>Server RESTART OP</codeName>\n      </serverInstanceOperation>\n      <serverInstanceStatusName>rebooting</serverInstanceStatusName>\n      <createDate>2024-05-26T14:30:13+0900</createDate>\n      <uptime>2024-05-27T18:55:18+0900</uptime>\n      <serverImageProductCode>SW.VSVR.OS.LNX64.UBNTU.SVR2004.B050</serverImageProductCode>\n      <serverProductCode>SVR.VSVR.HICPU.C002.M004.NET.SSD.B050.G002</serverProductCode>\n      <isProtectServerTermination>false</isProtectServerTermination>\n      <zoneCode>KR-1</zoneCode>\n      <regionCode>KR</regionCode>\n      <vpcNo>5119753</vpcNo>\n      <subnetNo>19238</subnetNo>\n      <networkInterfaceNoList>\n        <networkInterfaceNo>348071</networkInterfaceNo>\n      </networkInterfaceNoList>\n      <initScriptNo></initScriptNo>\n      <serverInstanceType>\n        <code>HICPU</code>\n        <codeName>High CPU</codeName>\n      </serverInstanceType>\n      <baseBlockStorageDiskType>\n        <code>NET</code>\n        <codeName>Network Storage</codeName>\n      </baseBlockStorageDiskType>\n      <baseBlockStorageDiskDetailType>\n        <code>SSD</code>\n        <codeName>SSD</codeName>\n      </baseBlockStorageDiskDetailType>\n      <placementGroupNo></placementGroupNo>\n      <placementGroupName></placementGroupName>\n      <memberServerImageInstanceNo>3051719</memberServerImageInstanceNo>\n      <hypervisorType>\n        <code>XEN</code>\n        <codeName>XEN</codeName>\n      </hypervisorType>\n      <serverImageNo>3051719</serverImageNo>\n      <serverSpecCode>c2-g2-s50</serverSpecCode>\n    </serverInstance>\n  </serverInstanceList>\n</rebootServerInstancesResponse>"
    }
  }
}
```
- raw 값이 xml이 아닌 json 값으로 변경 부탁드립니다.


## resourceinfo {update, get, set}
### resourceinfo.get
#### resourceinfo.get.request
```
request resourceinfo.get
{
  "request": {
    "id": "124ba750-a5ca-45e2-b9c4-083c5e4b8132",
    "code": "resourceinfo",
    "parameter": {
      "command": "get",
      "data": {}
    }
  }
}
```
#### resourceinfo.get.response
```
response resourceinfo.get
{
  "response": {
    "id": "124ba750-a5ca-45e2-b9c4-083c5e4b8132",
    "code": "resourceinfo",
    "message": "success",
    "reason": "",
    "data": {
      "resource": "{\"accesscontrolgroup\": {\"columns\": 
          ..중략...
          \"\\ud3c9\\ucd0c zone\"]]}}"
    }
  }
}
```
- resource 가 최상단 키값이 아닌 `"resource": { "raw": {} }` 이걸로 부탁드립니다.


### resourceinfo.set
#### resourceinfo.set.request
```
request resourceinfo.set
{
  "request": {
    "id": "683288ca-a766-41bc-b166-6d27232f6142",
    "code": "resourceinfo",
    "parameter": {
      "command": "set",
      "data": {
        "resource": "{\"accesscontrolgroup\": {\"columns\": ... 중략 ...
\"KR-1\", \"\\ud3c9\\ucd0c zone\"]]}}"
      }
    }
  }
}
```
- resource 가 최상단 키값이 아닌 `"resource": { "raw": {} }` 이걸로 부탁드립니다.

#### resourceinfo.set.response
```
response resourceinfo.set
{
  "response": {
    "id": "683288ca-a766-41bc-b166-6d27232f6142",
    "code": "resourceinfo",
    "message": "success",
    "reason": "",
    "data": {}
  }
}
```

### resourceinfo.update
#### resourceinfo.update.request
```
request resourceinfo.update
{
  "request": {
    "id": "8fa886d5-4b87-48a4-88ab-ab2f53bd6e6f",
    "code": "resourceinfo",
    "parameter": {
      "command": "update",
      "data": {
        "plan": {
          "id": 1,
          "name": "DR_DEMO_001",
          "instance": [
            {
              "uuid": "3051792",
              "name": "s18fb360bc62"
            }
          ]
        },
        "recovery": {
          "raw": {
            "table_name": "serverinstance",
            "column_name": "servername",
            "uuid": 1,
            "new_value": "updated_name"
          }
        }
      }
    }
  }
}
```

#### resourceinfo.update.response
```
response resourceinfo
{
  "response": {
    "id": "8fa886d5-4b87-48a4-88ab-ab2f53bd6e6f",
    "code": "resourceinfo",
    "message": "success",
    "reason": "",
    "data": {
      "resource": "table name: serverinstance, column name: servername, old_value: 3051792, new_value: updated_name"
    }
  }
}
```
- **resourceinfo 의 update 는 없습니다.**

## recoveryinfo {set, get, delete, status, update}
- set이 제일 먼저 들어갑니다.

### recoveryinfo.get
#### recoveryinfo.get.request
```
request recoveryinfo.get
{
  "request": {
    "id": "082b9982-14ce-4a9f-bc26-2fc4b8943a2f",
    "code": "recoveryinfo",
    "parameter": {
      "command": "get",
      "data": {}
    }
  }
}
```
- recoveryinfo.get.request 부분에 "data" 값이 비어있는데 여기에 plan 값이 들어가는게 맞습니다. (response에 적혀있는 부분의 값이 request로
  오고 recoveryinfo 정의한 값을 response에 넣어야합니다.)

#### recoveryinfo.get.response
```
response recoveryinfo
{
  "response": {
    "id": "082b9982-14ce-4a9f-bc26-2fc4b8943a2f",
    "code": "recoveryinfo",
    "message": "success",
    "reason": "",
    "data": [
      {
        "plan": {
          "id": 1,
          "name": "DR_DEMO_001",
          "instance": [
            {
              "uuid": "3051792",
              "name": "s18fb360bc62"
            }
          ]
        }
      }
    ]
  }
}
```
- data 는 리스트가 아닙니다.
- 여기엔 plan으로 감싸여져 있는게 아닌 `recovery` 데이터를 정의하여 주셔야합니다.
- 혹시 recovery 정의한 값이 있을까요?

### recoveryinfo.set
#### recoveryinfo.set.request
```
request recoveryinfo.set
{
  "request": {
    "id": "cc51d40b-aa3c-4f18-b692-50c8fa5b7b34",
    "code": "recoveryinfo",
    "parameter": {
      "command": "set",
      "data": {
        "plan": {
          "id": "DR_DEMO_001",
          "name": "DR_DEMO_001",
          "instance": [
            {
              "requestid": "DR_DEMO_001",
              "resourcetype": "serverinstance",
              "sourcekey": "3051792",
              "timestamp": "2024-06-13 13:17:34",
              "command": "CREATE",
              "detail": null,
              "completeflag": false
            }
          ]
        }
      }
    }
  }
}
```
- id 값은 string이 아닌 int값입니다.
- instance 리스트엔 uuid와 name 값이 들어갑니다.(instance 리스트의 value 는 어떻게 정의된건가요?)

#### recoveryinfo.set.response
```
response recoveryinfo
{
  "response": {
    "id": "cc51d40b-aa3c-4f18-b692-50c8fa5b7b34",
    "code": "recoveryinfo",
    "message": "success",
    "reason": "",
    "data": {}
  }
}
```

### recoveryinfo.update
#### recoveryinfo.update.request
```
request recoveryinfo.update
{
  "request": {
    "id": "7319555a-f482-437a-befd-b9113b2f370a",
    "code": "recoveryinfo",
    "parameter": {
      "command": "update",
      "data": {
        "plan": {
          "id": 1,
          "name": "DR_DEMO_001",
          "instance": [
            {
              "uuid": "3051792",
              "name": "s18fb360bc62"
            }
          ]
        },
        "recovery": {
          "raw": {
            "table_name": "serverinstance",
            "column_name": "servername",
            "uuid": 1,
            "new_value": "updated_name"
          }
        }
      }
    }
  }
}
```
- 위에서 질문한 대로 recovery 를 정의한 값이 없을까요?
- raw에 다 들어 가 있는게 아닌 정의된 값이 필요합니다.

#### recoveryinfo.update.response
```
response recoveryinfo
{
  "response": {
    "id": "7319555a-f482-437a-befd-b9113b2f370a",
    "code": "recoveryinfo",
    "message": "success",
    "reason": "",
    "data": {
      "resource": "table name: serverinstance, column name: servername, old_value: 3051792, new_value: updated_name"
    }
  }
}
```
- 응답값이 resource 만 오는게 아니라 변경값이 적용된 전체 값이 있어야 하지않을까요?

### recoveryinfo.status
#### recoveryinfo.status.request
```
request recoveryinfo.status
{
  "request": {
    "id": "b7ef0136-f2bd-4e96-ac34-fdbdc95fe976",
    "code": "recoveryinfo",
    "parameter": {
      "command": "status",
      "data": {}
    }
  }
}
```
- 어떤 plan의 상태값을 원하는지 plan 정보가 있어야 하지 않나요?
- 위에서 설명 했던 plan 정보가 들어가야합니다.

#### recoveryinfo.status.response
```
response recoveryinfo
{
  "response": {
    "id": "b7ef0136-f2bd-4e96-ac34-fdbdc95fe976",
    "code": "recoveryinfo",
    "message": "success",
    "reason": "",
    "data": [
      {
        "plan": {
          "id": 1,
          "name": "DR_DEMO_001",
          "instance": [
            {
              "uuid": "3051792",
              "name": "new_name"
            }
          ]
        }
      }
    ]
  }
}
```
- data 값은 리스트가 아닙니다.
- 응답 데이터엔 recovery 관련 리소스 상태를 나타내는 구조 정의가 필요합니다.

### recoveryinfo.delete
#### recoveryinfo.delete.request
```
request recoveryinfo.delete
{
  "request": {
    "id": "7a4e3ea2-9ca0-4ba2-9580-55ed81c9f7ca",
    "code": "recoveryinfo",
    "parameter": {
      "command": "delete",
      "data": {
        "plan": {
          "id": 1,
          "name": "target-A"
        }
      }
    }
  }
}
```
#### recoveryinfo.delete.response
```
response recoveryinfo
{
  "response": {
    "id": "7a4e3ea2-9ca0-4ba2-9580-55ed81c9f7ca",
    "code": "recoveryinfo",
    "message": "success",
    "reason": "",
    "data": {
      "result": "Plan id: 1 deleted successfully"
    }
  }
}
```

## recoveryjob {rollback, pause, stop, run}
### recoveryjob.run
#### recoveryjob.run.request
```
request recoveryjob.run
{
  "request": {
    "id": "4ad98375-e18f-48c6-87fc-05b911b10c58",
    "code": "recoveryjob",
    "parameter": {
      "command": "run",
      "data": {
        "instance": {
          "plan": {
            "id": 1,
            "name": "target-A"
          }
        }
      }
    }
  }
}
```
- instance 가 제일 상단에서 묶어놨는데 plan이 제일 최상단에 **`job_id` 가 들어가야합니다.** (instance 가 없어야합니다.)

#### recoveryjob.run.response
```
response recoveryjob
{
  "response": {
    "id": "4ad98375-e18f-48c6-87fc-05b911b10c58",
    "code": "recoveryjob",
    "message": "success",
    "reason": "",
    "data": "success"
  }
}
```

### recoveryjob.pause
#### recoveryjob.pause.request
```
-
```
#### recoveryjob.pause.response
```

```

### recoveryjob.stop
- stop 은 구현필요
#### recoveryjob.stop.request
```
-
```
#### recoveryjob.stop.response
```

```

### recoveryjob.rollback
#### recoveryjob.rollback.request
```
request recoveryjob.rollback
{
  "request": {
    "id": "d8a2fb46-63e8-4a31-a58c-2bb02f99f99b",
    "code": "recoveryjob",
    "parameter": {
      "command": "rollback",
      "data": {
        "instance": {
          "plan": {
            "id": 1,
            "name": "target-A"
          }
        }
      }
    }
  }
}
```
- - instance 가 제일 상단에서 묶어놨는데 plan이 제일 최상단에 **`job_id` 가 들어가야합니다.** (instance 가 없어야합니다.)
- 
#### recoveryjob.rollback.response
```
response recoveryjob
{
  "response": {
    "id": "d8a2fb46-63e8-4a31-a58c-2bb02f99f99b",
    "code": "recoveryjob",
    "message": "success",
    "reason": "",
    "data": ""
  }
}
```

## volumeinfo {create_sanpshot_volume, delete, get, attach, create, detach}
### volumeinfo.get
#### volumeinfo.get.request
```
request volumeinfo.get
{
  "request": {
    "id": "c5187413-9c36-42f2-a34a-e352291b4d65",
    "code": "volumeinfo",
    "parameter": {
      "command": "get",
      "data": {
        "instance": []
      }
    }
  }
}
```
- instance로 리스트를 묶는게 아니라 instance_volume 으로 묶어야합니다.
- instance 의 uuid 가 없습니다.

#### volumeinfo.get.response
```
response volumeinfo
{
  "response": {
    "id": "c5187413-9c36-42f2-a34a-e352291b4d65",
    "code": "volumeinfo",
    "message": "success",
    "reason": "",
    "data": {
      "instance": [
        {
          "instance": {
            "uuid": "3081226"
          },
          "volume": [
            {
              "uuid": "3081227",
              "name": "s18fb360bc62",
              "type": "SSD",
              "size": 53687091200,
              "status": "attached",
              "raw": {
                "blockstorageinstance": {
                  "blockstorageinstanceno": "3081227"
                }
              }
            }
          ]
        }
      ]
    }
  }
}
```
- instance로 리스트를 묶는게 아니라 instance_volume 으로 묶어야합니다.

### volumeinfo.create
#### volumeinfo.create.request
```
request volumeinfo.create
{
  "request": {
    "id": "b5013d74-409f-41f8-8969-c2415054914f",
    "code": "volumeinfo",
    "parameter": {
      "command": "create",
      "data": {
        "instance": [
          {
            "uuid": "3081226"
          }
        ]
      }
    }
  }
}
```
- instance_volume 으로 묶고 instance 값만 있는게 아닌 volume의 type과 size 값도 넣어야합니다.

#### volumeinfo.create.response
```
response volumeinfo
{
  "response": {
    "id": "b5013d74-409f-41f8-8969-c2415054914f",
    "code": "volumeinfo",
    "message": "success",
    "reason": "",
    "data": {
      "serverinstanceno": "3081226",
      "blockstorageinstanceno": "3183443",
      "raw": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<createBlockStorageInstanceResponse>\n  <requestId>74953c5b-6c3c-4a26-b04f-b8efdd1c6e24</requestId>\n  <returnCode>0</returnCode>\n  <returnMessage>success</returnMessage>\n  <totalRows>1</totalRows>\n  <blockStorageInstanceList>\n    <blockStorageInstance>\n      <blockStorageInstanceNo>3183443</blockStorageInstanceNo>\n      <serverInstanceNo>3081226</serverInstanceNo>\n      <blockStorageName>bst1901b0c4823</blockStorageName>\n      <blockStorageType>\n        <code>SVRBS</code>\n        <codeName>Server BS</codeName>\n      </blockStorageType>\n      <blockStorageSize>107374182400</blockStorageSize>\n      <deviceName></deviceName>\n      <blockStorageProductCode>SPBSTBSTAD000006</blockStorageProductCode>\n      <blockStorageInstanceStatus>\n        <code>INIT</code>\n        <codeName>Block Storage INIT State</codeName>\n      </blockStorageInstanceStatus>\n      <blockStorageInstanceOperation>\n        <code>NULL</code>\n        <codeName>Block Storage NULL OP</codeName>\n      </blockStorageInstanceOperation>\n      <blockStorageInstanceStatusName>initialized</blockStorageInstanceStatusName>\n      <createDate>2024-06-15T17:38:28+0900</createDate>\n      <blockStorageDescription></blockStorageDescription>\n      <blockStorageDiskType>\n        <code>NET</code>\n        <codeName>Network Storage</codeName>\n      </blockStorageDiskType>\n      <blockStorageDiskDetailType>\n        <code>SSD</code>\n        <codeName>SSD</codeName>\n      </blockStorageDiskDetailType>\n      <maxIopsThroughput>4000</maxIopsThroughput>\n      <isEncryptedVolume>false</isEncryptedVolume>\n      <zoneCode>KR-1</zoneCode>\n      <regionCode>KR</regionCode>\n      <isReturnProtection>false</isReturnProtection>\n      <blockStorageVolumeType>\n        <code>SSD</code>\n        <codeName>SSD</codeName>\n      </blockStorageVolumeType>\n      <hypervisorType>\n        <code>XEN</code>\n        <codeName>XEN</codeName>\n      </hypervisorType>\n    </blockStorageInstance>\n  </blockStorageInstanceList>\n</createBlockStorageInstanceResponse>"
    }
  }
}
```
- 응답 값에도 instance_volume 으로 묶고 serverinstanceno 값은 instance 의 uuid 에 넣고 blockstorageinstanceno 값은 volume 의 uuid 에 넣고 raw도 volume에 넣어야 하지않나요?

### volumeinfo.create_sanpshot_volume
#### volumeinfo.create_sanpshot_volume.request
```
request volumeinfo.create_snapshot_volume
{
  "request": {
    "id": "de4669a3-78d4-4044-8d14-6f9093774a77",
    "code": "volumeinfo",
    "parameter": {
      "command": "create_snapshot_volume",
      "data": {
        "instance": [
          {
            "uuid": "3081227"
          }
        ]
      }
    }
  }
}
```
- instance_volume 에 감싸여진 instance 와 volume 이 있고 volume 리스트안에 volume uuid 가 있고 snapshot 리스트가 있습니다. 이곳에 snapshot의 uuid 값이 들어가야합니다.
- 이 api 로 생성된 볼륨을 가지고 특정 인스턴스에 attach 가 가능한지 기능점검 부탁드립니다.

#### volumeinfo.create_sanpshot_volume.response
```
response volumeinfo
{
  "response": {
    "id": "de4669a3-78d4-4044-8d14-6f9093774a77",
    "code": "volumeinfo",
    "message": "success",
    "reason": "",
    "data": {
      "blockstoragesnapshotinstanceno": "3183468",
      "originalblockstorageinstanceno": "3081227",
      "raw": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<createBlockStorageSnapshotInstanceResponse>\n  <requestId>a24ea78f-c7b4-46b4-b7dd-1cc16b735f2b</requestId>\n  <returnCode>0</returnCode>\n  <returnMessage>success</returnMessage>\n  <totalRows>1</totalRows>\n  <blockStorageSnapshotInstanceList>\n    <blockStorageSnapshotInstance>\n      <blockStorageSnapshotInstanceNo>3183468</blockStorageSnapshotInstanceNo>\n      <blockStorageSnapshotName>sh1901b16230a</blockStorageSnapshotName>\n      <blockStorageSnapshotVolumeSize>53687091200</blockStorageSnapshotVolumeSize>\n      <originalBlockStorageInstanceNo>3081227</originalBlockStorageInstanceNo>\n      <blockStorageSnapshotInstanceStatus>\n        <code>INIT</code>\n        <codeName>Block Storage INIT State</codeName>\n      </blockStorageSnapshotInstanceStatus>\n      <blockStorageSnapshotInstanceOperation>\n        <code>CREAT</code>\n        <codeName>Block storage CREATE OP</codeName>\n      </blockStorageSnapshotInstanceOperation>\n      <blockStorageSnapshotInstanceStatusName>creating</blockStorageSnapshotInstanceStatusName>\n      <createDate>2024-06-15T17:49:14+0900</createDate>\n      <isEncryptedOriginalBlockStorageVolume>false</isEncryptedOriginalBlockStorageVolume>\n      <blockStorageSnapshotDescription></blockStorageSnapshotDescription>\n      <snapshotType>\n        <code>FULL</code>\n        <codeName>Full Storage Snapshot</codeName>\n      </snapshotType>\n      <baseSnapshotInstanceNo></baseSnapshotInstanceNo>\n      <snapshotChainDepth>0</snapshotChainDepth>\n      <isBootable>false</isBootable>\n      <hypervisorType>\n        <code>XEN</code>\n        <codeName>XEN</codeName>\n      </hypervisorType>\n    </blockStorageSnapshotInstance>\n  </blockStorageSnapshotInstanceList>\n</createBlockStorageSnapshotInstanceResponse>"
    }
  }
}
```

### volumeinfo.delete
#### volumeinfo.delete.request
```
request volumeinfo.delete
{
  "request": {
    "id": "fba44b2a-539b-45f5-ae08-5647b86f8abb",
    "code": "volumeinfo",
    "parameter": {
      "command": "delete",
      "data": {
        "instance": [
          {
            "uuid": "3183443"
          }
        ]
      }
    }
  }
}
```
- instance의 volume uuid 가 필요하기 때문에 instance_volume 이 감싸진 값이 필요합니다. (위에 설명한 값)

#### volumeinfo.delete.response
```
response volumeinfo
{
  "response": {
    "id": "fba44b2a-539b-45f5-ae08-5647b86f8abb",
    "code": "volumeinfo",
    "message": "success",
    "reason": "",
    "data": {
      "blockstorageinstanceno": "3183443",
      "raw": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<deleteBlockStorageInstancesResponse>\n  <requestId>e75b1ff8-d02f-4b28-8c7e-bd45a5c88b7d</requestId>\n  <returnCode>0</returnCode>\n  <returnMessage>success</returnMessage>\n  <totalRows>1</totalRows>\n  <blockStorageInstanceList>\n    <blockStorageInstance>\n      <blockStorageInstanceNo>3183443</blockStorageInstanceNo>\n      <serverInstanceNo></serverInstanceNo>\n      <blockStorageName>bst1901b0c4823</blockStorageName>\n      <blockStorageType>\n        <code>SVRBS</code>\n        <codeName>Server BS</codeName>\n      </blockStorageType>\n      <blockStorageSize>107374182400</blockStorageSize>\n      <deviceName></deviceName>\n      <blockStorageProductCode>SPBSTBSTAD000006</blockStorageProductCode>\n      <blockStorageInstanceStatus>\n        <code>CREAT</code>\n        <codeName>Block Storage CREATED State</codeName>\n      </blockStorageInstanceStatus>\n      <blockStorageInstanceOperation>\n        <code>TERMT</code>\n        <codeName>Block Storage TERMINATE OP</codeName>\n      </blockStorageInstanceOperation>\n      <blockStorageInstanceStatusName>terminating</blockStorageInstanceStatusName>\n      <createDate>2024-06-15T17:38:28+0900</createDate>\n      <blockStorageDescription></blockStorageDescription>\n      <blockStorageDiskType>\n        <code>NET</code>\n        <codeName>Network Storage</codeName>\n      </blockStorageDiskType>\n      <blockStorageDiskDetailType>\n        <code>SSD</code>\n        <codeName>SSD</codeName>\n      </blockStorageDiskDetailType>\n      <maxIopsThroughput>4000</maxIopsThroughput>\n      <isEncryptedVolume>false</isEncryptedVolume>\n      <zoneCode>KR-1</zoneCode>\n      <regionCode>KR</regionCode>\n      <isReturnProtection>false</isReturnProtection>\n      <blockStorageVolumeType>\n        <code>SSD</code>\n        <codeName>SSD</codeName>\n      </blockStorageVolumeType>\n      <hypervisorType>\n        <code>XEN</code>\n        <codeName>XEN</codeName>\n      </hypervisorType>\n    </blockStorageInstance>\n  </blockStorageInstanceList>\n</deleteBlockStorageInstancesResponse>"
    }
  }
}
```

### volumeinfo.attach
#### volumeinfo.attach.request
```
request volumeinfo.attach
{
  "request": {
    "id": "44e51e05-7629-460c-983c-842563ab155f",
    "code": "volumeinfo",
    "parameter": {
      "command": "attach",
      "data": {
        "instance": [
          {
            "volume_uuid": "3183443",
            "instance_uuid": "3081226"
          }
        ]
      }
    }
  }
}
```
-  instance로 묶는게 아닌 instance_volume 으로 묶어야 하는데 volume을 한개만 하는게 아니기때문에 volume을 리스트로 해야합니다.
```json
"instance_volume": [
                {
                // this 인스턴스에
                    "instance": {
                        "uuid": "serverinstance.serverinstanceno"
                    },
                // 어떤 볼륨을 붙이겠다.
                    "volume": [
                        {
                            "uuid": "blockstorageinstance.blockstorageinstanceno",
                            "name": "blockstorageinstance.blockstoragename",
                            "type": "blockstorageinstance.blockstoragediskdetailtype",
                            "size": "blockstorageinstance.blockstoragesize",
                            "status": "blockstorageinstance.blockstorageinstancestatusname",
                            "snapshot" []                            
                            "raw": {
                                "blockstorageinstance": {
                                    "blockstorageinstanceno": "blockstorageinstance.blockstorageinstanceno"
                                }
                            }
                        }
                    ]
                }
            ]
```

#### volumeinfo.attach.response
```
response volumeinfo
{
  "response": {
    "id": "44e51e05-7629-460c-983c-842563ab155f",
    "code": "volumeinfo",
    "message": "success",
    "reason": "",
    "data": {
      "serverinstanceno": "3081226",
      "blockstorageinstanceno": "3183443",
      "raw": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<attachBlockStorageInstanceResponse>\n  <requestId>3e54d2c0-04bf-4d91-b778-dd47292b985d</requestId>\n  <returnCode>0</returnCode>\n  <returnMessage>success</returnMessage>\n  <totalRows>1</totalRows>\n  <blockStorageInstanceList>\n    <blockStorageInstance>\n      <blockStorageInstanceNo>3183443</blockStorageInstanceNo>\n      <serverInstanceNo>3081226</serverInstanceNo>\n      <blockStorageName>bst1901b0c4823</blockStorageName>\n      <blockStorageType>\n        <code>SVRBS</code>\n        <codeName>Server BS</codeName>\n      </blockStorageType>\n      <blockStorageSize>107374182400</blockStorageSize>\n      <deviceName></deviceName>\n      <blockStorageProductCode>SPBSTBSTAD000006</blockStorageProductCode>\n      <blockStorageInstanceStatus>\n        <code>CREAT</code>\n        <codeName>Block Storage CREATED State</codeName>\n      </blockStorageInstanceStatus>\n      <blockStorageInstanceOperation>\n        <code>ATTAC</code>\n        <codeName>Block Storage  STOP OP</codeName>\n      </blockStorageInstanceOperation>\n      <blockStorageInstanceStatusName>attaching</blockStorageInstanceStatusName>\n      <createDate>2024-06-15T17:38:28+0900</createDate>\n      <blockStorageDescription></blockStorageDescription>\n      <blockStorageDiskType>\n        <code>NET</code>\n        <codeName>Network Storage</codeName>\n      </blockStorageDiskType>\n      <blockStorageDiskDetailType>\n        <code>SSD</code>\n        <codeName>SSD</codeName>\n      </blockStorageDiskDetailType>\n      <maxIopsThroughput>4000</maxIopsThroughput>\n      <isEncryptedVolume>false</isEncryptedVolume>\n      <zoneCode>KR-1</zoneCode>\n      <regionCode>KR</regionCode>\n      <isReturnProtection>false</isReturnProtection>\n      <blockStorageVolumeType>\n        <code>SSD</code>\n        <codeName>SSD</codeName>\n      </blockStorageVolumeType>\n      <hypervisorType>\n        <code>XEN</code>\n        <codeName>XEN</codeName>\n      </hypervisorType>\n    </blockStorageInstance>\n  </blockStorageInstanceList>\n</attachBlockStorageInstanceResponse>"
    }
  }
}
```
- 아래의 구조체로 표현 부탁드립니다.
```json
"instance_volume": [
                {
                    // this 인스턴스에
                    "instance": {
                        "uuid": "serverinstance.serverinstanceno"
                    },
                    // 어떤 볼륨을 붙이겠다.
                    "volume": [
                        {
                            "uuid": "blockstorageinstance.blockstorageinstanceno",
                            "name": "blockstorageinstance.blockstoragename",
                            "type": "blockstorageinstance.blockstoragediskdetailtype",
                            "size": "blockstorageinstance.blockstoragesize",
                            "status": "blockstorageinstance.blockstorageinstancestatusname",
                            "snapshot" []                            
                            "raw": {
                                "blockstorageinstance": {
                                    "blockstorageinstanceno": "blockstorageinstance.blockstorageinstanceno"
                                }
                            }
                        }
                    ]
                }
            ]
```

### volumeinfo.detach
#### volumeinfo.detach.request
```
request volumeinfo.detach
{
  "request": {
    "id": "689b4062-96fb-4544-986a-544fa6b5ded6",
    "code": "volumeinfo",
    "parameter": {
      "command": "detach",
      "data": {
        "instance": [
          {
            "uuid": "3183443"
          }
        ]
      }
    }
  }
}
```


#### volumeinfo.detach.response
```
response volumeinfo
{
  "response": {
    "id": "689b4062-96fb-4544-986a-544fa6b5ded6",
    "code": "volumeinfo",
    "message": "success",
    "reason": "",
    "data": {
      "serverinstanceno": "3081226",
      "blockstorageinstanceno": "3183443",
      "raw": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<detachBlockStorageInstancesResponse>\n  <requestId>7a3ffea6-f7b7-442a-836c-091b6b2227a6</requestId>\n  <returnCode>0</returnCode>\n  <returnMessage>success</returnMessage>\n  <totalRows>1</totalRows>\n  <blockStorageInstanceList>\n    <blockStorageInstance>\n      <blockStorageInstanceNo>3183443</blockStorageInstanceNo>\n      <serverInstanceNo>3081226</serverInstanceNo>\n      <blockStorageName>bst1901b0c4823</blockStorageName>\n      <blockStorageType>\n        <code>SVRBS</code>\n        <codeName>Server BS</codeName>\n      </blockStorageType>\n      <blockStorageSize>107374182400</blockStorageSize>\n      <deviceName>/dev/xvdb</deviceName>\n      <blockStorageProductCode>SPBSTBSTAD000006</blockStorageProductCode>\n      <blockStorageInstanceStatus>\n        <code>ATTAC</code>\n        <codeName>Block storage ATTACHED state</codeName>\n      </blockStorageInstanceStatus>\n      <blockStorageInstanceOperation>\n        <code>DETAC</code>\n        <codeName>Block Storage RESTART OP</codeName>\n      </blockStorageInstanceOperation>\n      <blockStorageInstanceStatusName>detaching</blockStorageInstanceStatusName>\n      <createDate>2024-06-15T17:38:28+0900</createDate>\n      <blockStorageDescription></blockStorageDescription>\n      <blockStorageDiskType>\n        <code>NET</code>\n        <codeName>Network Storage</codeName>\n      </blockStorageDiskType>\n      <blockStorageDiskDetailType>\n        <code>SSD</code>\n        <codeName>SSD</codeName>\n      </blockStorageDiskDetailType>\n      <maxIopsThroughput>4000</maxIopsThroughput>\n      <isEncryptedVolume>false</isEncryptedVolume>\n      <zoneCode>KR-1</zoneCode>\n      <regionCode>KR</regionCode>\n      <isReturnProtection>false</isReturnProtection>\n      <blockStorageVolumeType>\n        <code>SSD</code>\n        <codeName>SSD</codeName>\n      </blockStorageVolumeType>\n      <hypervisorType>\n        <code>XEN</code>\n        <codeName>XEN</codeName>\n      </hypervisorType>\n    </blockStorageInstance>\n  </blockStorageInstanceList>\n</detachBlockStorageInstancesResponse>"
    }
  }
}
```
```json
"instance_volume": [
                {
                    "instance": {
                        "uuid": "serverinstance.serverinstanceno"
                    },
                    "volume": [
                        {
                            "uuid": "blockstorageinstance.blockstorageinstanceno",
                            "name": "blockstorageinstance.blockstoragename",
                            "type": "blockstorageinstance.blockstoragediskdetailtype",
                            "size": "blockstorageinstance.blockstoragesize",
                            "status": "blockstorageinstance.blockstorageinstancestatusname",
                            "snapshot" []                            
                            "raw": {
                                "blockstorageinstance": {
                                    "blockstorageinstanceno": "blockstorageinstance.blockstorageinstanceno"
                                }
                            }
                        }
                    ]
                }
            ]
```

## snapshotinfo {delete, create, get}
### snapshotinfo.get
#### snapshotinfo.get.request
```
request snapshotinfo.get
{
  "request": {
    "id": "35b1611b-b9d3-444c-b2be-094e63d114ca",
    "code": "snapshotinfo",
    "parameter": {
      "command": "get",
      "data": {
        "instance": []
      }
    }
  }
}
```
- instance_volume 로 묶어야 합니다.
- 전체 정보를 요청할 땐 `"data": {}` 로 보내고
- instance_volume 에 감싸여진 instance 의 uuid 만 있으면 특정 인스턴스의 volume snapshot 정보를 보내고
- volume uuid 정보가 있으면 특정 인스턴스의 볼륨의 스냅샷 정보를 보내고
- snapshot uuid 정보가 있으면 특정 스냅샷 정보를 보내주셔야 합니다.

#### snapshotinfo.get.response
```
response snapshotinfo
{
  "response": {
    "id": "35b1611b-b9d3-444c-b2be-094e63d114ca",
    "code": "snapshotinfo",
    "message": "success",
    "reason": "",
    "data": {
      "instance": [
        {
          "instance": {
            "uuid": ""
          },
          "volume": [
            {
              "uuid": 3081227,
              "snapshot": [
                {
                  "uuid": "3183468",
                  "name": "sh1901b16230a",
                  "size": 53687091200,
                  "status": "created",
                  "type": "FULL",
                  "date": "2024-06-15T17:49:14",
                  "raw": {
                    "blockstoragesnapshotinstance": {
                      "blockstoragesnapshotinstanceno": "3183468"
                    }
                  }
                }
              ]
            }
          ]
        }
      ]
    }
  }
}
```
- 제일 상단의 값은 instance가 아니라 instance_volume 입니다.

### snapshotinfo.create
#### snapshotinfo.create.request
```
-
```
#### snapshotinfo.create.response
```

```

### snapshotinfo.delete
#### snapshotinfo.delete.request
```
request snapshotinfo.delete
{
  "request": {
    "id": "9f92f7a4-11b6-43d7-b17b-952dc8af903b",
    "code": "snapshotinfo",
    "parameter": {
      "command": "delete",
      "data": {
        "instance": [
          {
            "uuid": "3183468"
          }
        ]
      }
    }
  }
}
```
- instance_volume 로 묶어야 합니다.
- instance_volume 에 감싸여진 instance 의 uuid 만 있으면 특정 인스턴스의 volume snapshot 을 삭제하고
- volume uuid 정보가 있으면 특정 인스턴스의 볼륨의 스냅샷을 삭제하고
- snapshot uuid 정보가 있으면 특정 스냅샷을 삭제해야 합니다.

#### snapshotinfo.delete.response
```
response snapshotinfo
{
  "response": {
    "id": "9f92f7a4-11b6-43d7-b17b-952dc8af903b",
    "code": "snapshotinfo",
    "message": "success",
    "reason": "",
    "data": {
      "blockstoragesnapshotinstanceno": "3183468",
      "originalblockstorageinstanceno": "3081227",
      "raw": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<deleteBlockStorageSnapshotInstancesResponse>\n  <requestId>c499ad74-fea2-4a9c-a2b2-cb77646e937f</requestId>\n  <returnCode>0</returnCode>\n  <returnMessage>success</returnMessage>\n  <totalRows>1</totalRows>\n  <blockStorageSnapshotInstanceList>\n    <blockStorageSnapshotInstance>\n      <blockStorageSnapshotInstanceNo>3183468</blockStorageSnapshotInstanceNo>\n      <blockStorageSnapshotName>sh1901b16230a</blockStorageSnapshotName>\n      <blockStorageSnapshotVolumeSize>53687091200</blockStorageSnapshotVolumeSize>\n      <originalBlockStorageInstanceNo>3081227</originalBlockStorageInstanceNo>\n      <blockStorageSnapshotInstanceStatus>\n        <code>CREAT</code>\n        <codeName>Block Storage CREATED State</codeName>\n      </blockStorageSnapshotInstanceStatus>\n      <blockStorageSnapshotInstanceOperation>\n        <code>TERMT</code>\n        <codeName>Block Storage TERMINATE OP</codeName>\n      </blockStorageSnapshotInstanceOperation>\n      <blockStorageSnapshotInstanceStatusName>terminating</blockStorageSnapshotInstanceStatusName>\n      <createDate>2024-06-15T17:49:14+0900</createDate>\n      <isEncryptedOriginalBlockStorageVolume>false</isEncryptedOriginalBlockStorageVolume>\n      <blockStorageSnapshotDescription></blockStorageSnapshotDescription>\n      <snapshotType>\n        <code>FULL</code>\n        <codeName>Full Storage Snapshot</codeName>\n      </snapshotType>\n      <baseSnapshotInstanceNo></baseSnapshotInstanceNo>\n      <snapshotChainDepth>0</snapshotChainDepth>\n      <isBootable>false</isBootable>\n      <hypervisorType>\n        <code>XEN</code>\n        <codeName>XEN</codeName>\n      </hypervisorType>\n    </blockStorageSnapshotInstance>\n  </blockStorageSnapshotInstanceList>\n</deleteBlockStorageSnapshotInstancesResponse>"
    }
  }
}
```

**사전 정의가 필요한 데이터 요청입니다.**
- RecoveryInfo
  - 인스턴스 중심으로 데이터를 구성하되, dr이 필요한 리소스들의 종속관계를 잡아서 표현해주세요.
- RecoveryInfo Status