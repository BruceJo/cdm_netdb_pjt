def urlInfo():
    return {
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
        "InAutoScalingGroupServerInstance" : {
            "api_url" : "vautoscaling/v2",
            "read" : "getAutoScalingGroupList"
        },
        "AdjustmentType" : {
            "api_url" : "vautoscaling/v2",
            "read" : "getAdjustmentTypeList"
        },
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
        # "MemberServerImageInstanceList" : {
        #     "api_url" : "vserver/v2",
        #     "read" : "getMemberServerImageInstanceList"
        # },
    }