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
        # "Product" : {   # {'error': {'errorCode': '300', 'message': 'Not Found Exception', 'details': 'URL not found.'}}
        #     "api_url" : "billing/v1/product",
        #     "read" : "getProductList"
        # }
        # "MemberServerImage" : {   # 뭔가 이상
        #     "api_url" : "vserver/v2",
        #     "read" : "getMemberServerImageInstanceList"
        # },
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
        }
    }