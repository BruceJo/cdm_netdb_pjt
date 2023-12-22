def url_info():
    return {
        # 중권
        "RouteTable" : {
            "api_url" : "vpc/v2",
            "create" : "createRouteTable",
            "read" : "getRouteTableList",
            "update" : "setRouteTableDescription",
            "delete" : "deleteRouteTable"
        },
        "Route" : {
            "api_url" : "vpc/v2", 
            "create" : "addRoute",
            "read" : "getRouteList"
        },
        "PlacementGroup" : {
            "api_url" : "vserver/v2",
            "create" : "createPlacementGroup",
            "read" : "getPlacementGroupList",
            "delete" : "deletePlacementGroup"
        },
        "LaunchConfiguration" : {
            "api_url" : "vautoscaling/v2",
            "create" : "createLaunchConfiguration",
            "read" : "getLaunchConfigurationList",
            "delete" : "deleteLaunchConfiguration"
        },
        "InAutoScalingGroupServerInstance" : {  #자원 개수에 따른 루프 확인 필요
            "api_url" : "vautoscaling/v2",
            "read" : "getAutoScalingGroupList"
        },
        "AdjustmentType" : {
            "api_url" : "vautoscaling/v2",
            "read" : "getAdjustmentTypeList"
        },
        # 현병
        "LoginKey" : {
            "api_url" : "vserver/v2",
            "read" : "getLoginKeyList"
        },
        "ServerInstance" : {
            "api_url" : "vserver/v2",
            "read" : "getServerInstanceList"
        },
        "Product" : {
            "api_url" : "billing/v1/product",
            "read" : "getProductList"
        },
        "MemberServerImageInstance" : {
            "api_url" : "vserver/v2",
            "read" : "getMemberServerImageInstanceList"
        },
        # 우동
        "AutoScalingGroup" : {
            "api_url" : "vautoscaling/v2",
            "read" : "getAutoScalingGroupList"
        },
        "NatGatewayInstance" : {
            "api_url" : "vpc/v2",
            "read" : "getNatGatewayInstanceList"
        },
        "NetworkAcl" : {
            "api_url" : "vpc/v2",
            "read" : "getNetworkAclList"
        },
        "NetworkAclDenyAllowGroup" : {
            "api_url" : "vpc/v2",
            "read" : "getNetworkAclDenyAllowGroupList"
        },
        "Vpc" : {
            "api_url" : "vpc/v2",
            "read" : "getVpcList"
        },
        "Subnet" : {
            "api_url" : "vpc/v2",
            "read" : "getSubnetList"
        },
        "ActivityLog" : {
            "api_url" : "vautoscaling/v2",
            "read" : "getAutoScalingActivityLogList"
        },
        "NetworkAclRule" : {
            "api_url" : "vpc/v2",
            "read" : "getNetworkAclRuleList"
        },
        "ScalingPolicy" : {
            "api_url" : "vautoscaling/v2",
            "read" : "getAutoScalingPolicyList"
        },
        "ScheduledUpdateGroupAction" : {
            "api_url" : "vautoscaling/v2",
            "read" : "getScheduledActionList"
        },
        "BlockStorageInstance" : {
            "api_url" : "vserver/v2",
            "read" : "getBlockStorageInstanceList"
        },
        "BlockStorageSnapshotInstance" : {
            "api_url" : "vserver/v2",
            "read" : "getBlockStorageSnapshotInstanceList"
        },
        "NetworkInterface" : {
            "api_url" : "vserver/v2",
            "read" : "getNetworkInterfaceList"
        },
        "PublicIpInstance" : {
            "api_url" : "vserver/v2",
            "read" : "getPublicIpInstanceList"
        },
        "VpcPeeringInstance" : {
            "api_url" : "vpc/v2",
            "read" : "getVpcPeeringInstanceList"
        },
        # 상우
        "AccessControlGroup" : {
            "api_url" : "vserver/v2",
            "read" : "getAccessControlGroupList"
        },
        "AccessControlGroupRule" : {
            "api_url" : "vserver/v2",
            "read" : "getAccessControlGroupRuleList"
        },
        "InitScript" : {
            "api_url" : "vserver/v2",
            "read" : "getInitScriptList"
        },
    }

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
        }
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
        InitScript = ['osType']
    )

def out_candidate():
    return dict(
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
        vpcpeeringinstance = ['targetVpcName', 'sourceVpcIpv4CidrBlock', 'targetVpcIpv4CidrBlock', 'sourceVpcName', 'sourceVpcNo', 'targetVpcNo']
    )

def col_name_mapper():
    return {
        'common' : {
            'regionCode' : 'regionid',
            'vpcNo' : 'vpcid',
            'loginKeyName' : 'loginkeyid',
            'zoneCode' : 'zoneid',
            'subnetNo' : 'subnetid',
            'originalServerInstanceNo' : 'originalserverinstanceid',
            'networkAclNo' : 'networkaclid',
            'originalBlockStorageInstanceNo' : 'blockstorageinstanceid',
            'productItemKind' : 'producttype',
            'targetVpcNo' : 'targetvpcid',
            'sourceVpcNo' : 'sourcevpcid'
        },
        'launchconfiguration' : {
            'serverProductCode' : 'serverproductid'
        },
        'serverinstance' : {
            'serverProductCode' : 'serverproductcodeid'
        }
    }