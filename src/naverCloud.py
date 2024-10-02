############################################
# Common Info                              #
############################################

def get_ordered_table_list():
    return {        
        "accesscontrolgroup": 1,
        "adjustmenttype": 2,
        "inautoscalinggroupserverinstance": 3,
        "initscript": 4,
        "loadbalancerruleaction": 5,
        "loadbalancerrulecondition": 6,
        "loginkey": 7,
        "memberserverimageinstance": 8,
        "placementgroup": 9,
        "product": 10,
        "protocoltype": 11,
        "publicipinstance": 12,
        "region": 13,
        "accesscontrolgrouprule": 14,
        "launchconfiguration": 15,
        "vpc": 16,
        "vpcpeeringinstance": 17,
        "zone": 18,
        "blockstorageinstance": 19,
        "blockstoragesnapshotinstance": 20,
        "loadbalancerinstance": 21,
        "loadbalancerlistener": 22,
        "loadbalancerrule": 23,
        "memberserverimage": 24,
        "networkacl": 25,
        "networkacldenyallowgroup": 26,
        "networkaclrule": 27,
        "routetable": 28,
        "subnet": 29,
        "autoscalinggroup": 30,
        "loadbalancersubnet": 31,
        "natgatewayinstance": 32,
        "networkinterface": 33,
        "route": 34,
        "scalingpolicy": 35,
        "scheduledupdategroupaction": 36,
        "serverinstance": 37,
        "activitylog": 38,
        "targetgroup": 39
    }

def url_info():
    return {
        ### step.2 https://api-gov.ncloud-docs.com/docs/home에서 본인 api의 주소를 작성
        "Region" : {
            "api_url" : "vserver/v2",
            "read" : "getRegionList"
        },
        "Zone" : {
            "api_url" : "vserver/v2",
            "read" : "getZoneList"
        },        
        "AdjustmentType" : {
            "api_url" : "vautoscaling/v2",
            "read" : "getAdjustmentTypeList"
        },
        "InAutoScalingGroupServerInstance" : {
            "api_url" : "vautoscaling/v2",
            "read" : "getAutoScalingGroupList"
        },
        "InitScript" : {
            "api_url" : "vserver/v2",
            "read" : "getInitScriptList",
            "create" : "createInitScript"
        },
        "LoadBalancerRuleAction" : {
            "api_url" : "vloadbalancer/v2",
            "read" : "getLoadBalancerRuleList"
        },
        "LoadBalancerRuleCondition" : {
            "api_url" : "vloadbalancer/v2",
            "read" : "getLoadBalancerRuleList"
        },
        "Vpc" : {
            "api_url" : "vpc/v2",
            "read" : "getVpcList",
            "create" : "createVpc",
            "delete" : "deleteVpc"
        },
        "AccessControlGroup" : {
            "api_url" : "vserver/v2",
            "read" : "getAccessControlGroupList",
            "create" : "createAccessControlGroup"
        },
        "VpcPeeringInstance" : {
            "api_url" : "vpc/v2",
            "read" : "getVpcPeeringInstanceList",
            "create" : "createVpcPeeringInstance",
            "delete" : "deleteVpcPeeringInstance",
            "update" : ["acceptOrRejectVpcPeering","setVpcPeeringDescription"]
        },
        "NetworkAclDenyAllowGroup" : {
            "api_url" : "vpc/v2",
            "read" : "getNetworkAclDenyAllowGroupList",
            "create" : "createNetworkAclDenyAllowGroup",
            "delete" : "deleteNetworkAclDenyAllowGroup",
        },
        "NetworkAcl" : {
            "api_url" : "vpc/v2",
            "read" : "getNetworkAclList",
            "create" : "createNetworkAcl",
            "delete" : "deleteNetworkAcl",
        },
        "LoadBalancerInstance" : {
            "api_url" : "vloadbalancer/v2",
            "read" : "getLoadBalancerInstanceList",
            "create" : "createLoadBalancerInstance",
            "delete" : "deleteLoadBalancerInstances",
            "update" : ["changeLoadBalancerInstanceConfiguration", "setLoadBalancerInstanceSubnet"]
        },
        "RouteTable" : {
            "api_url" : "vpc/v2",
            "create" : "createRouteTable",
            "read" : "getRouteTableList",
            "update" : "setRouteTableDescription",
            "delete" : "deleteRouteTable"
        },
        "LoginKey" : {
            "api_url" : "vserver/v2",
            "read" : "getLoginKeyList"
        },
        "AccessControlGroupRule" : {
            "api_url" : "vserver/v2",
            "read" : "getAccessControlGroupRuleList",
            "update" : ["addAccessControlGroupInboundRule", "addAccessControlGroupOutboundRule"]
        },        
        "Product" : {
            "api_url" : "billing/v1/product",
            "read" : "getProductList"
        },
        "NetworkAclRule" : {
            "api_url" : "vpc/v2",
            "read" : "getNetworkAclRuleList"
        },
        "PlacementGroup" : {
            "api_url" : "vserver/v2",
            "create" : "createPlacementGroup",
            "read" : "getPlacementGroupList",
            "delete" : "deletePlacementGroup"
        },
        "Subnet" : {
            "api_url" : "vpc/v2",
            "read" : "getSubnetList",
            "create" : "createSubnet",
            "delete" : "deleteSubnet"
        },
        "LoadBalancerListener" : {
            "api_url" : "vloadbalancer/v2",
            "read" : "getLoadBalancerListenerList",
            "create" : "createLoadBalancerListener",
            "delete" : "deleteLoadBalancerListeners",
            "update" : "changeLoadBalancerListenerConfiguration"
        },
        "PublicIpInstance" : {
            "api_url" : "vserver/v2",
            "read" : "getPublicIpInstanceList",
            "create" : "createPublicIpInstance",
            "update" : ["associatePublicIpWithServerInstance","disassociatePublicIpFromServerInstance"],
            "delete" : "deletePublicIpInstance"
        },
        "Route" : {
            "api_url" : "vpc/v2", 
            "create" : "addRoute",
            "read" : "getRouteList"
        },
        "BlockStorageInstance" : {
            "api_url" : "vserver/v2",
            "read" : "getBlockStorageInstanceList",
            "create" : "createBlockStorageInstance",
            "update": ["changeBlockStorageVolumeSize","attachBlockStorageInstance",
                       "detachBlockStorageInstances","setBlockStorageReturnProtection"],
            "delete" : "deleteBlockStorageInstances"
        },
        "LaunchConfiguration" : {
            "api_url" : "vautoscaling/v2",
            "create" : "createLaunchConfiguration",
            "read" : "getLaunchConfigurationList",
            "delete" : "deleteLaunchConfiguration"
        },
        "ServerInstance" : {
            "api_url" : "vserver/v2",
            "read" : "getServerInstanceList",
            "create" : "createServerInstances"
        },
        "AutoScalingGroup" : {
            "api_url" : "vautoscaling/v2",
            "read" : "getAutoScalingGroupList",            
            "create" : "createAutoScalingGroup",
            "delete" : "deleteAutoScalingGroup",
            "update" : "updateAutoScalingGroup",  
        },
        "MemberServerImageInstance" : {
            "api_url" : "vserver/v2",
            "read" : "getMemberServerImageInstanceList"
        },
        "NetworkInterface" : {
            "api_url" : "vserver/v2",
            "read" : "getNetworkInterfaceList",
            "create" : "createNetworkInterface",
            "delete" : "deleteNetworkInterface",
            "update" : ["attachNetworkInterface", "detachNetworkInterface","addNetworkInterfaceAccessControlGroup","removeNetworkInterfaceAccessControlGroup"]  
        },
        "NatGatewayInstance" : {
            "api_url" : "vpc/v2",
            "read" : "getNatGatewayInstanceList",
            "create" : "createNatGatewayInstance",
            "delete" : "deleteNatGatewayInstance"
        },
        "LoadBalancerSubnet" : {
            "api_url" : "vloadbalancer/v2",
            "read" : "getLoadBalancerInstanceList"
        },
        "LoadBalancerRule" : {
            "api_url" : "vloadbalancer/v2",
            "read" : "getLoadBalancerRuleList"
        },
        "BlockStorageSnapshotInstance" : {
            "api_url" : "vserver/v2",
            "read" : "getBlockStorageSnapshotInstanceList",
            "create" : "createBlockStorageSnapshotInstance",
            "delete" : "deleteBlockStorageSnapshotInstances"
        },
        "ActivityLog" : {
            "api_url" : "vautoscaling/v2",
            "read" : "getAutoScalingActivityLogList"
        },
        "ScalingPolicy" : {
            "api_url" : "vautoscaling/v2",
            "read" : "getAutoScalingPolicyList",
            "create" : "putScalingPolicy",
            "delete" : "deleteScalingPolicy",
            "update" : "putScalingPolicy"
        },
        "ScheduledUpdateGroupAction" : {
            "api_url" : "vautoscaling/v2",
            "read" : "getScheduledActionList",
            "create" : "putScheduledUpdateGroupAction",
            "delete" : "deleteScheduledAction",
            "update" : "putScheduledUpdateGroupAction"
        },
        "TargetGroup": {
            "api_url": "vloadbalancer/v2",
            "read": "getTargetGroupList",
            "create": "createTargetGroup"
        }
    }

def set_url(name, action, *choice):
    nc = url_info()
    nc = {k.lower() : v for k, v in nc.items()}
    try:
        table_name = name.lower()
        action = action[0].lower()
    except:
        table_name = name
        action = action[0]
        
    if action == "c":
        api_url, sub_url = nc[table_name]["api_url"], nc[table_name]["create"]
    elif action == "r":
        api_url, sub_url = nc[table_name]["api_url"], nc[table_name]["read"]
    elif action == "u":
        api_url, sub_url = nc[table_name]["api_url"], nc[table_name]["update"]
    elif action == "d":
        api_url, sub_url = nc[table_name]["api_url"], nc[table_name]["delete"]
    
    if isinstance(sub_url, list):
        if choice:
            sub_url = choice[0]
        else:
            raise NameError(sub_url)

    return table_name, api_url, sub_url

############################################
# Read to Insert Info                      #
############################################

def special_info():
    return {
        "route" : {
            "table" : ["vpc v", "routetable r"],
            "where" : ["v.id = r.vpcid"],
            "value" : ["v.vpcno", "r.routetableno", "r.id"],
            "stage" : "routeList",
            "fetch" : {
                "vpcNo" : "row['vpcno']",
                "routeTableNo" : "row['routetableno']"
            }
        },
        "activitylog" : {
            "table" : ["autoscalinggroup"],
            "where" : [],
            "value" : ["autoscalinggroupno"],
            "stage" : "activityLogList",
            "fetch" : {
                "autoScalingGroupNo" : "row['autoscalinggroupno']"
            }
        },
        "networkaclrule" : {
            "table" : ["networkacl"],
            "where" : [],
            "value" : ["networkaclno"],
            "stage" : "networkAclRuleList",
            "fetch" : {
                "networkAclNo" : "row['networkaclno']"
            }
        },
        "scalingpolicy" : {
            "table" : ["autoscalinggroup"],
            "where" : [],
            "value" : ["autoscalinggroupno"],
            "stage" : "scalingPolicyList",
            "fetch" : {
                "autoScalingGroupNo" : "row['autoscalinggroupno']"
            }
        },
        "scheduledupdategroupaction" : {
            "table" : ["autoscalinggroup"],
            "where" : [],
            "value" : ["autoscalinggroupno"],
            "stage" : "scheduledUpdateGroupActionList",
            "fetch" : {
                "autoScalingGroupNo" : "row['autoscalinggroupno']"
            }
        },
        "accesscontrolgrouprule" : {
            "table" : ["accesscontrolgroup"],
            "where" : [],
            "value" : ["accesscontrolgroupno"],
            "stage" : "accessControlGroupRuleList",
            "fetch" : {
                "accessControlGroupNo" : "row['accesscontrolgroupno']"
            }
        },
        "loadbalancerlistener" : {
            "table" : ["loadbalancerinstance"],
            "where" : [],
            "value" : ["loadbalancerinstanceno"],
            "stage" : "loadBalancerListenerList",
            "fetch" : {
                "loadBalancerInstanceNo" : "row['loadbalancerinstanceno']"
            }
        },
        "loadbalancerrule" : {
            "table" : ["loadbalancerlistener"],
            "where" : [],
            "value" : ["loadbalancerlistenerno"],
            "stage" : "loadBalancerRuleList",
            "fetch" : {
                "loadBalancerListenerNo" : "row['loadbalancerlistenerno']"
            }
        },
        "loadbalancerruleaction" : {
            "table" : ["loadbalancerlistener"],
            "where" : [],
            "value" : ["loadbalancerlistenerno"],
            "stage" : "loadBalancerRuleList",
            "fetch" : {
                "loadBalancerListenerNo" : "row['loadbalancerlistenerno']"
            }
        },
        "loadbalancerrulecondition" : {
            "table" : ["loadbalancerlistener"],
            "where" : [],
            "value" : ["loadbalancerlistenerno"],
            "stage" : "loadBalancerRuleList",
            "fetch" : {
                "loadBalancerListenerNo" : "row['loadbalancerlistenerno']"
            }
        },
    }

def code_candidate():
    return dict(
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
        Subnet = ['subnetStatus', 'subnetType', 'usageType'],
        BlockStorageInstance = ['blockStorageType', 'blockStorageInstanceStatus', 'blockStorageInstanceOperation', 'blockStorageDiskYype', 'blockStorageDiskDetailType', 'blockStorageDiskType'],
        BlockStorageSnapshotInstance = ['blockStorageSnapshotInstanceStatus', 'blockStorageSnapshotInstanceOperation', 'snapshotType'],
        NetworkInterface = ['networkInterfaceStatus', 'instanceType'],
        PublicIpInstance = ['publicIpInstanceStatus', 'publicIpInstanceOperation'],
        VpcPeeringInstance = ['vpcPeeringInstanceStatus', 'vpcPeeringInstanceOperation'],
        AccessControlGroup = ['accessControlGroupStatus'],
        InitScript = ['osType'],
        LoadBalancerInstance = ['loadBalancerInstanceStatus', 'loadBalancerInstanceOperation', 'loadBalancerType', 'loadBalancerNetworkType', 'throughputType']
    )

def out_candidate():
    return dict(
        region = ['zoneName', 'zoneDescription'],
        zone = ['regionCode'],
        routetable = ['vpcNo', 'regionCode'],
        launchconfiguration = ['regionCode', 'serverProductCode', 'loginKeyName'],
        inautoscalinggroupserverinstance = ['regionCode', 'serverProductCode', 'loginKeyName'],
        serverinstance = ['serverProductCode', 'hypervisorType', 'serverImageNo', 'serverSpecCode', 'zoneCode', 'regionCode', 'vpcNo', 'subnetNo'],
        memberserverimageinstance = ['originalServerImageProductCode', 'originalServerInstanceNo', 'originalServerInstanceProductCode'],
        autoscalinggroup = ['vpcNo', 'vpcName', 'zoneCode', 'subnetName', 'subnetNo'],
        natgatewayinstance = ['vpcNo', 'vpcName', 'zoneCode', 'subnetName', 'subnetNo'],
        vpc = ['regionCode'],
        subnet = ['vpcNo', 'zoneCode'],
        blockstorageinstance = ['blockStorageVolumeType', 'hypervisorType'],
        blockstoragesnapshotinstance = ['originalBlockStorageInstanceNo', 'isBootable'],
        networkinterface = ['enableFlowLog'],
        product = ['productItemKind', 'productItemKindDetail', 'softwareType'],
        vpcpeeringinstance = ['targetVpcName', 'sourceVpcIpv4CidrBlock', 'targetVpcIpv4CidrBlock', 'sourceVpcName', 'sourceVpcNo', 'targetVpcNo'],
        loadbalancersubnet = ['publicIpInstanceNo']
    )

def col_name_mapper():
    return {
        'common' : {
            'regionCode' : 'regionid',
            'vpcNo' : 'vpcid',
            'loginKeyName' : 'loginkeyid',
            'zoneCode' : 'zoneid',
            'subnetNo' : 'subnetno',
            'originalServerInstanceNo' : 'originalserverinstanceid',
            'networkAclNo' : 'networkaclid',
            'originalBlockStorageInstanceNo' : 'blockstorageinstanceid',
            'productItemKind' : 'producttype',
            'targetVpcNo' : 'targetvpcid',
            'sourceVpcNo' : 'sourcevpcid',
            'targetType': 'targetType',
            'targetGroupProtocolType': 'targetGroupProtocolType',
            'algorithmType': 'algorithmType',
            'healthCheckProtocolType': 'healthCheckProtocolType',
            'healthCheckHttpMethodType': 'healthCheckHttpMethodType',
            'publicIpInstanceNo' : 'publicipinstanceid'
        },
        'launchconfiguration' : {
            'serverProductCode' : 'serverproductid'
        },
        'serverinstance' : {
            'serverProductCode' : 'serverproductcodeid'
        },
        'targetgroup': {
            'serverProductCode': 'serverproductcodeid'
        }
    }

def init_table_rows():
    return {
        'protocoltype' : [
            {'code' : 'err', 'codename' : 'err', 'codenumber' : 0},
            {'code' : 'tcp', 'codename' : 'tcp', 'codenumber' : 1},
            {'code' : 'icmp', 'codename' : 'icmp', 'codenumber' : 2},
            {'code' : 'udp', 'codename' : 'udp', 'codenumber' : 3}
        ]
    }

############################################
# Create Info                              #
############################################

def include_keys(): #전체 키
    return {
        ### step.3 https://api-gov.ncloud-docs.com/docs/home에서 본인 api의 요청 파라미터를 작성
        # 단, regionCode와 responseFormatType는 제외한다
        'loginkey' : [], #free
        'serverinstance' : ['serverProductCode','serverImageProductCode','vpcNo','subnetNo', 'networkInterfaceNoList'], #pay
        'memberserverimageinstance' : ['memberServerImageInstanceNo', ''], #pay
        'routetable' : ['vpcNo', 'routeTableName', 'supportedSubnetTypeCode', 'routeTableDescription'], 
        'blockstorageinstance' : ['zoneCode', 'blockStorageName', 'blockStorageDiskDetailTypeCode', 'blockStorageVolumeTypeCode', 
                                  'serverInstanceNo', 'blockStorageSnapshotInstanceNo', 'blockStorageSize', 'blockStorageDescription', 'isReturnProtection'],
        'publicipinstance' : ['serverInstanceNo', 'publicIpDescription'],
        # 단, regionCode와 responseFormatType는 제외한다
        'loadbalancerinstance' : ['loadBalancerTypeCode', 'loadBalancerName', 'loadBalancerNetworkTypeCode', 'throughputTypeCode', 'idleTimeout', 'vpcNo', 'subnetNoList.N', 'loadBalancerListenerList.N.targetGroupNo', 'loadBalancerSubnetList.N.publicIpInstanceNo'], #pay
        'loadbalancerlistener' : ['loadBalancerInstanceNo', 'protocolTypeCode', 'port', 'targetGroupNo', 'useHttp2'], #pay
        'blockstoragesnapshotinstance' : ['originalBlockStorageInstanceNo','blockStorageSnapshotName','blockStorageSnapshotDescription','snapshotTypeCode'],
        'vpcpeeringinstance':['vpcPeeringName','sourceVpcNo','targetVpcNo','targetVpcName','targetVpcLoginId','vpcPeeringDescription'], #pay
        'networkinterface' : ['vpcNo','subnetNo','networkInterfaceName','accessControlGroupNoList','serverInstanceNo','ip','secondaryIpList.N','secondaryIpCount','networkInterfaceDescription'],
        'launchconfiguration' : ['serverImageProductCode', 'memberServerImageInstanceNo', 'serverProductCode', 'isEncryptedVolume', 'initScriptNo', 'launchConfigurationName', 'loginKeyName'],
        'natgatewayinstance' : ['zoneCode', 'vpcNo','subnetNo'],
        'targetgroup' : ["vpcNo", "targetGroupName", "targetTypeCode", "targetGroupProtocolTypeCode", "targetGroupPort", "targetGroupDescription",
                         "healthCheckProtocolTypeCode", "healthCheckPort", "healthCheckUrlPath", "healthCheckHttpMethodTypeCode",
                         "healthCheckCycle", "healthCheckUpThreshold", "healthCheckDownThreshold", "targetNoList.N"],
        'vpc' : ['vpcName','ipv4CidrBlock'], #free
        'placementgroup' : ['placementGroupName', 'placementGroupTypeCode'],
        'networkacl' : ['vpcNo'],
        'scheduledactionlist' : ['autoScalingGroupNo','scheduledActionName','minSize','maxSize','desiredCapacity','startTime','endTime','recurrence','timeZone'],
        'networkacldenyallowgroup' : ['vpcNo','networkAclDenyAllowGroupName'],
        'initscript' : ['initScriptName','initScriptContent','osTypeCode','initScriptDescription'],
        'accesscontrolgroup' : ['vpcNo','accessControlGroupName','accessControlGroupDescription'], #free
        'networkaclrule' : ['networkAclNo','networkAclRuleList.N.protocolTypeCode','networkAclRuleList.N.portRange','networkAclRuleList.N.ipBlock','networkAclRuleList.N.networkAclRuleDescription'], #404 free
        'accesscontrolgrouprule' : ['vpcNo','accessControlGroupNo', 'accessControlGroupRuleList.N.protocolTypeCode','accessControlGroupRuleList.N.portRange','accessControlGroupRuleList.N.ipBlock','accessControlGroupRuleList.N.accessControlGroupSequence','accessControlGroupRuleList.N.accessControlGroupRuleDescription'], #free       
        'subnet' : ['vpcNo', 'zoneCode', 'networkAclNo', 'subnetName', 'subnet', 'subnetTypeCode', 'usageType'], #406 free
        'route' : ['vpcNo', 'routeTableNo', 'routeList.N.destinationCidrBlock', 'routeList.N.gatewayTypeCode', 'routeList.N.gatewayId', 'routeList.N.routeDescription'], #408 free
        'scalingpolicy' : ['autoScalingGroupNo','scalingPolicyName','adjustmentTypeCode','adjustmentValue','adjustmentCooldown','scalingPolicyAction','scalingPolicyStatus'], #601 free
        'autoscalinggroup' : ['launchConfigurationNo','vpcNo','subnetNo','accessControlGroupNoList','minSize','maxSize']
        
    }

        #'autoscalinggroup' : ['launchConfigurationNo','autoScalingGroupName','serverNamePrefix','desiredCapacity','defaultCoolDown','healthCheckGracePeriod','healthCheckTypeCode','vpcNo','subnetNo','accessControlGroupNoList','minSize','maxSize'],

# def include_keys(): # 무료 자원에 대한 키
#     return {
#         'initscript': ['initScriptName','initScriptContent','osTypeCode','initScriptDescription'], #0
#         'vpc' : ['vpcName','ipv4CidrBlock'], #200 free
#         'accesscontrolgroup' : ['vpcNo','accessControlGroupName','accessControlGroupDescription'], #300 free
#         'networkacldenyallowgroup' : ['vpcNo','networkAclDenyAllowGroupName'], #303 free
#         'networkacl' : ['vpcNo','networkAclName'], #304 free
#         'routetable' : ['vpcNo', 'routeTableName', 'supportedSubnetTypeCode', 'routeTableDescription'], #306 free
#         'loginkey' : [], #400 free
#         'accesscontrolgrouprule': ['vpcNo','accessControlGroupNo', 'accessControlGroupRuleList.N.protocolTypeCode','accessControlGroupRuleList.N.portRange','accessControlGroupRuleList.N.ipBlock','accessControlGroupRuleList.N.accessControlGroupSequence','accessControlGroupRuleList.N.accessControlGroupRuleDescription'], #401 free
#         # 'networkaclrule' : ['networkAclNo','networkAclRuleList.N.protocolTypeCode','networkAclRuleList.N.portRange','networkAclRuleList.N.ipBlock','networkAclRuleList.N.networkAclRuleDescription'], #404 free
#         'placementgroup' : ['placementGroupName', 'placementGroupTypeCode'], #405 free
#         # 'subnet' : ['vpcNo', 'subnetName', 'subnet', 'subnetTypeCode', 'usageTypeCode', 'subnetDescription'], #406 free
#         # 'route' : ['vpcNo', 'routeTableNo', 'routeList.N.destinationCidrBlock', 'routeList.N.gatewayTypeCode', 'routeList.N.gatewayId', 'routeList.N.routeDescription'], #408 free
#         'launchconfiguration' : ['serverImageProductCode', 'memberServerImageInstanceNo', 'serverProductCode', 'isEncryptedVolume', 'initScriptNo', 'launchConfigurationName', 'loginKeyName'], #500 free
#         'autoscalinggroup' : ['launchConfigurationNo','vpcNo','subnetNo','accessControlGroupNoList','minSize','maxSize'], #502 free
#         # 'scalingpolicy' : ['autoScalingGroupNo','scalingPolicyName','adjustmentTypeCode','adjustmentValue','adjustmentCooldown','scalingPolicyAction','scalingPolicyStatus'], #601 free
#     }
