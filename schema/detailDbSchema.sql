CREATE SEQUENCE IF NOT EXISTS accesscontrolgroup_seq;
CREATE SEQUENCE IF NOT EXISTS adjustmenttype_seq;
CREATE SEQUENCE IF NOT EXISTS inautoscalinggroupserverinstance_seq;
CREATE SEQUENCE IF NOT EXISTS initscript_seq;
CREATE SEQUENCE IF NOT EXISTS loadbalancerruleaction_seq;
CREATE SEQUENCE IF NOT EXISTS loadbalancerrulecondition_seq;
CREATE SEQUENCE IF NOT EXISTS loginkey_seq;
CREATE SEQUENCE IF NOT EXISTS memberserverimageinstance_seq;
CREATE SEQUENCE IF NOT EXISTS placementgroup_seq;
CREATE SEQUENCE IF NOT EXISTS product_seq;
CREATE SEQUENCE IF NOT EXISTS protocoltype_seq;
CREATE SEQUENCE IF NOT EXISTS publicipinstance_seq;
CREATE SEQUENCE IF NOT EXISTS region_seq;
CREATE SEQUENCE IF NOT EXISTS accesscontrolgrouprule_seq;
CREATE SEQUENCE IF NOT EXISTS launchconfiguration_seq;
CREATE SEQUENCE IF NOT EXISTS vpc_seq;
CREATE SEQUENCE IF NOT EXISTS vpcpeeringinstance_seq;
CREATE SEQUENCE IF NOT EXISTS zone_seq;
CREATE SEQUENCE IF NOT EXISTS blockstorageinstance_seq;
CREATE SEQUENCE IF NOT EXISTS blockstoragesnapshotinstance_seq;
CREATE SEQUENCE IF NOT EXISTS loadbalancerinstance_seq;
CREATE SEQUENCE IF NOT EXISTS loadbalancerlistener_seq;
CREATE SEQUENCE IF NOT EXISTS loadbalancerrule_seq;
CREATE SEQUENCE IF NOT EXISTS memberserverimage_seq;
CREATE SEQUENCE IF NOT EXISTS networkacl_seq;
CREATE SEQUENCE IF NOT EXISTS networkacldenyallowgroup_seq;
CREATE SEQUENCE IF NOT EXISTS networkaclrule_seq;
CREATE SEQUENCE IF NOT EXISTS routetable_seq;
CREATE SEQUENCE IF NOT EXISTS subnet_seq;
CREATE SEQUENCE IF NOT EXISTS autoscalinggroup_seq;
CREATE SEQUENCE IF NOT EXISTS loadbalancersubnet_seq;
CREATE SEQUENCE IF NOT EXISTS natgatewayinstance_seq;
CREATE SEQUENCE IF NOT EXISTS networkinterface_seq;
CREATE SEQUENCE IF NOT EXISTS route_seq;
CREATE SEQUENCE IF NOT EXISTS scalingpolicy_seq;
CREATE SEQUENCE IF NOT EXISTS scheduledupdategroupaction_seq;
CREATE SEQUENCE IF NOT EXISTS serverinstance_seq;
CREATE SEQUENCE IF NOT EXISTS activitylog_seq;
CREATE SEQUENCE IF NOT EXISTS targetgroup_seq;


CREATE TABLE IF NOT EXISTS accesscontrolgroup (
	id INTEGER NOT NULL DEFAULT NEXTVAL('accesscontrolgroup_seq'),
	accesscontrolgroupno VARCHAR(255) NOT NULL,
	accesscontrolgroupname VARCHAR(255) NOT NULL,
	isdefault BOOL NOT NULL,
	vpcno VARCHAR(255) NOT NULL,
	accesscontrolgroupstatus VARCHAR(255) NOT NULL,
	accesscontrolgroupdescription VARCHAR(255) NULL,
	CONSTRAINT accesscontrolgroup_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS adjustmenttype (
	id INTEGER NOT NULL DEFAULT NEXTVAL('adjustmenttype_seq'),
	code VARCHAR(255) NOT NULL,
	codename VARCHAR(255) NOT NULL,
	CONSTRAINT adjustmenttype_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS inautoscalinggroupserverinstance (
	id INTEGER NOT NULL DEFAULT NEXTVAL('inautoscalinggroupserverinstance_seq'),
	serverinstanceno VARCHAR(255) NULL,
	healthstatus VARCHAR(255) NULL,
	lifecyclestate VARCHAR(255) NULL,
	CONSTRAINT inautoscalinggroupserverinstance_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS initscript (
	id INTEGER NOT NULL DEFAULT NEXTVAL('initscript_seq'),
	initscriptno VARCHAR(255) NOT NULL,
	initscriptname VARCHAR(255) NOT NULL,
	createdate TIMESTAMP NOT NULL,
	initscriptdescription VARCHAR(255) NULL,
	initscriptcontent TEXT NOT NULL,
	ostype VARCHAR(255) NOT NULL,
	CONSTRAINT initscript_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS loadbalancerruleaction (
	id INTEGER NOT NULL DEFAULT NEXTVAL('loadbalancerruleaction_seq'),
	ruleactiontype VARCHAR(255) NOT NULL,
	targetgroupaction VARCHAR(255) NULL,
	redirectionaction VARCHAR(255) NULL,
	CONSTRAINT loadbalancerruleaction_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS loadbalancerrulecondition (
	id INTEGER NOT NULL DEFAULT NEXTVAL('loadbalancerrulecondition_seq'),
	ruleconditiontype VARCHAR(255) NOT NULL,
	hostheadercondition VARCHAR(255) NULL,
	pathpatterncondition VARCHAR(255) NULL,
	CONSTRAINT loadbalancerrulecondition_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS loginkey (
	id INTEGER NOT NULL DEFAULT NEXTVAL('loginkey_seq'),
	fingerprint VARCHAR(255) NOT NULL,
	keyname VARCHAR(255) NOT NULL,
	createdate TIMESTAMP NOT NULL,
	CONSTRAINT loginkey_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS memberserverimageinstance (
	id INTEGER NOT NULL DEFAULT NEXTVAL('memberserverimageinstance_seq'),
	originalserverinstanceid INT8 NOT NULL,
	memberserverimageinstanceno VARCHAR(255) NOT NULL,
	memberserverimagename VARCHAR(255) NOT NULL,
	memberserverimagedescription VARCHAR(255) NULL,
	memberserverimageinstancestatus VARCHAR(255) NOT NULL,
	memberserverimageinstanceoperation VARCHAR(255) NOT NULL,
	memberserverimageinstancestatusname VARCHAR(255) NOT NULL,
	createdate TIMESTAMP NOT NULL,
	memberserverimageblockstoragetotalrows INT8 NOT NULL,
	memberserverimageblockstoragetotalsize INT8 NOT NULL,
	sharestatus VARCHAR(255) NOT NULL,
	sharedloginidlist JSONB NOT NULL,
	CONSTRAINT memberserverimageinstance_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS placementgroup (
	id INTEGER NOT NULL DEFAULT NEXTVAL('placementgroup_seq'),
	placementgroupno VARCHAR(255) NOT NULL,
	placementgroupname VARCHAR(255) NOT NULL,
	placementgrouptype VARCHAR(255) NOT NULL,
	CONSTRAINT placementgroup_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS product (
	id INTEGER NOT NULL DEFAULT NEXTVAL('product_seq'),
	productcode VARCHAR(255) NOT NULL,
	productname VARCHAR(255) NOT NULL,
	producttype VARCHAR(255) NOT NULL,
	productdescription VARCHAR(255) NOT NULL,
	infraresourcetype VARCHAR(255) NOT NULL,
	infraresourcedetailtype VARCHAR(255) NULL,
	cpucount INT8 NULL,
	memorysize INT8 NULL,
	baseblockstoragesize INT8 NULL,
	platformtype VARCHAR(255) NULL,
	osinformation VARCHAR(255) NULL,
	disktype VARCHAR(255) NULL,
	dbkindcode VARCHAR(255) NULL,
	addblockstoragesize INT8 NULL,
	generationcode VARCHAR(255) NULL,
	productcategory VARCHAR(255) NULL,
	CONSTRAINT product_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS protocoltype (
	id INTEGER NOT NULL DEFAULT NEXTVAL('protocoltype_seq'),
	code VARCHAR(255) NOT NULL,
	codename VARCHAR(255) NOT NULL,
	codenumber INT8 NOT NULL,
	CONSTRAINT protocoltype_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS publicipinstance (
	id INTEGER NOT NULL DEFAULT NEXTVAL('publicipinstance_seq'),
	publicipinstanceno VARCHAR(255) NOT NULL,
	publicip VARCHAR(255) NOT NULL,
	createdate TIMESTAMP NOT NULL,
	publicipdescription VARCHAR(255) NULL,
	publicipinstancestatusname VARCHAR(255) NOT NULL,
	publicipinstancestatus VARCHAR(255) NOT NULL,
	serverinstanceno VARCHAR(255) NULL,
	servername VARCHAR(255) NULL,
	privateip VARCHAR(255) NULL,
	lastmodifydate TIMESTAMP NULL,
	publicipinstanceoperation VARCHAR(255) NOT NULL,
	CONSTRAINT publicipinstance_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS region (
	id INTEGER NOT NULL DEFAULT NEXTVAL('region_seq'),
	regioncode VARCHAR(255) NOT NULL,
	regionname VARCHAR(255) NOT NULL,
	CONSTRAINT region_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS accesscontrolgrouprule (
	id INTEGER NOT NULL DEFAULT NEXTVAL('accesscontrolgrouprule_seq'),
	accesscontrolgroupid INT8 NOT NULL,
	accesscontrolgroupid_copy INT8 NULL,
	protocoltypeid INT8 NOT NULL,
	protocoltypeid_copy INT8 NULL,
	ipblock VARCHAR(255) NULL,
	accesscontrolgroupsequence VARCHAR(255) NULL,
	portrange VARCHAR(255) NULL,
	accesscontrolgroupruletype VARCHAR(255) NOT NULL,
	accesscontrolgroupruledescription VARCHAR(255) NOT NULL,
	CONSTRAINT accesscontrolgrouprule_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS launchconfiguration (
	id INTEGER NOT NULL DEFAULT NEXTVAL('launchconfiguration_seq'),
	regionid INT8 NOT NULL,
	regionid_copy INT8 NULL,
	serverproductid INT8 NOT NULL,
	serverproductid_copy INT8 NULL,
	loginkeyid INT8 NOT NULL,
	loginkeyid_copy INT8 NULL,
	launchconfigurationno VARCHAR(255) NOT NULL,
	launchconfigurationname VARCHAR(255) NOT NULL,
	serverimageproductcode VARCHAR(255) NULL,
	memberserverimageinstanceno VARCHAR(255) NULL,
	createdate DATE NOT NULL,
	launchconfigurationstatus VARCHAR(255) NOT NULL,
	initscriptno VARCHAR(255) NULL,
	isencryptedvolume BOOL NOT NULL,
	CONSTRAINT launchconfiguration_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS vpc (
	id INTEGER NOT NULL DEFAULT NEXTVAL('vpc_seq'),
	regionid INT8 NOT NULL,
	regionid_copy INT8 NULL,
	vpcno VARCHAR(255) NOT NULL,
	vpcname VARCHAR(255) NOT NULL,
	ipv4cidrblock VARCHAR(255) NOT NULL,
	vpcstatus VARCHAR(255) NOT NULL,
	createdate TIMESTAMP NOT NULL,
	CONSTRAINT vpc_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS vpcpeeringinstance (
	id INTEGER NOT NULL DEFAULT NEXTVAL('vpcpeeringinstance_seq'),
	regionid INT8 NOT NULL,
	regionid_copy INT8 NULL,
	sourcevpcid INT8 NOT NULL,
	sourcevpcid_copy INT8 NULL,
	targetvpcid INT8 NOT NULL,
	targetvpcid_copy INT8 NULL,
	vpcpeeringinstanceno VARCHAR(255) NOT NULL,
	vpcpeeringname VARCHAR(255) NOT NULL,
	regioncode VARCHAR(255) NOT NULL,
	createdate TIMESTAMP NOT NULL,
	lastmodifydate TIMESTAMP NOT NULL,
	vpcpeeringinstancestatus VARCHAR(255) NOT NULL,
	vpcpeeringinstancestatusname VARCHAR(255) NOT NULL,
	vpcpeeringinstanceoperation VARCHAR(255) NOT NULL,
	sourcevpcloginid VARCHAR(255) NOT NULL,
	targetvpcloginid VARCHAR(255) NOT NULL,
	vpcpeeringdescription VARCHAR(255) NULL,
	hasreversevpcpeering BOOL NOT NULL,
	isbetweenaccounts BOOL NOT NULL,
	reversevpcpeeringinstanceno VARCHAR(255) NULL,
	CONSTRAINT vpcpeeringinstance_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS zone (
	id INTEGER NOT NULL DEFAULT NEXTVAL('zone_seq'),
	regionid INT8 NOT NULL,
	regionid_copy INT8 NULL,
	zonename VARCHAR(255) NOT NULL,
	zonecode VARCHAR(255) NOT NULL,
	zonedescription VARCHAR(255) NOT NULL,
	CONSTRAINT zone_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS blockstorageinstance (
	id INTEGER NOT NULL DEFAULT NEXTVAL('blockstorageinstance_seq'),
	zoneid INT8 NOT NULL,
	zoneid_copy INT8 NULL,
	regionid INT8 NOT NULL,
	regionid_copy INT8 NULL,
	blockstorageinstanceno VARCHAR(255) NOT NULL,
	serverinstanceno VARCHAR(255) NULL,
	blockstoragename VARCHAR(255) NOT NULL,
	blockstoragetype VARCHAR(255) NOT NULL,
	blockstoragesize INT8 NOT NULL,
	devicename VARCHAR(255) NULL,
	blockstorageproductcode VARCHAR(255) NOT NULL,
	blockstorageinstancestatus VARCHAR(255) NOT NULL,
	blockstorageinstanceoperation VARCHAR(255) NOT NULL,
	blockstorageinstancestatusname VARCHAR(255) NOT NULL,
	createdate TIMESTAMP NOT NULL,
	blockstoragedescription VARCHAR(255) NULL,
	blockstoragedisktype VARCHAR(255) NOT NULL,
	blockstoragediskdetailtype VARCHAR(255) NOT NULL,
	maxiopsthroughput INT8 NULL,
	isencryptedvolume BOOL NOT NULL,
	isreturnprotection BOOL NOT NULL,
	CONSTRAINT blockstorageinstance_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS blockstoragesnapshotinstance (
	id INTEGER NOT NULL DEFAULT NEXTVAL('blockstoragesnapshotinstance_seq'),
	blockstorageinstanceid INT8 NOT NULL,
	blockstorageinstanceid_copy INT8 NULL,
	blockstoragesnapshotinstanceno VARCHAR(255) NOT NULL,
	blockstoragesnapshotname VARCHAR(255) NOT NULL,
	blockstoragesnapshotvolumesize INT8 NOT NULL,
	blockstoragesnapshotinstancestatus VARCHAR(255) NOT NULL,
	blockstoragesnapshotinstanceoperation VARCHAR(255) NOT NULL,
	blockstoragesnapshotinstancestatusname VARCHAR(255) NOT NULL,
	createdate TIMESTAMP NOT NULL,
	isencryptedoriginalblockstoragevolume BOOL NOT NULL,
	blockstoragesnapshotdescription VARCHAR(255) NULL,
	snapshottype VARCHAR(255) NOT NULL,
	basesnapshotinstanceno VARCHAR(255) NULL,
	snapshotchaindepth INT8 NOT NULL,
	CONSTRAINT blockstoragesnapshotinstance_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS loadbalancerinstance (
	id INTEGER NOT NULL DEFAULT NEXTVAL('loadbalancerinstance_seq'),
	vpcid INT8 NOT NULL,
	vpcid_copy INT8 NULL,
	regionid INT8 NOT NULL,
	regionid_copy INT8 NULL,
	loadbalancerinstanceno VARCHAR(255) NOT NULL,
	loadbalancerinstancestatus VARCHAR(255) NOT NULL,
	loadbalancerinstanceoperation VARCHAR(255) NOT NULL,
	loadbalancerinstancestatusname VARCHAR(255) NOT NULL,
	loadbalancerdescription TEXT NULL,
	createdate TIMESTAMP NOT NULL,
	loadbalancername VARCHAR(255) NOT NULL,
	loadbalancerdomain VARCHAR(255) NOT NULL,
	loadbalanceriplist JSONB NULL,
	loadbalancertype VARCHAR(255) NOT NULL,
	loadbalancernetworktype VARCHAR(255) NOT NULL,
	throughputtype VARCHAR(255) NOT NULL,
	idletimeout INT8 NULL,
	subnetnolist JSONB NOT NULL,
	loadbalancersubnetlist JSONB NOT NULL,
	loadbalancerlistenernolist JSONB NOT NULL,
	CONSTRAINT loadbalancerinstance_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS loadbalancerlistener (
	id INTEGER NOT NULL DEFAULT NEXTVAL('loadbalancerlistener_seq'),
	loadbalancerinstanceid INT8 NOT NULL,
	loadbalancerinstanceid_copy INT8 NULL,
	loadbalancerlistenerno VARCHAR(255) NOT NULL,
	protocoltype VARCHAR(50) NOT NULL,
	port INT8 NOT NULL,
	usehttp2 BOOL NOT NULL,
	sslcertificateno VARCHAR(255) NULL,
	tlsminversiontype VARCHAR(50) NULL,
	loadbalancerrulenolist JSONB NOT NULL,
	ciphersuitelist JSONB NOT NULL,
	CONSTRAINT loadbalancerlistener_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS loadbalancerrule (
	id INTEGER NOT NULL DEFAULT NEXTVAL('loadbalancerrule_seq'),
	loadbalancerlistenerid INT8 NOT NULL,
	loadbalancerlistenerid_copy INT8 NULL,
	loadbalancerruleno VARCHAR(255) NOT NULL,
	priority INT8 NOT NULL,
	loadbalancerruleconditionlist JSONB NOT NULL,
	loadbalancerruleactionlist JSONB NOT NULL,
	CONSTRAINT

 loadbalancerrule_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS memberserverimage (
	id INTEGER NOT NULL DEFAULT NEXTVAL('memberserverimage_seq'),
	originalserverinstanceid INT8 NOT NULL,
	zoneid INT8 NOT NULL,
	zoneid_copy INT8 NULL,
	memberserverimageno VARCHAR(255) NOT NULL,
	memberserverimagename VARCHAR(255) NOT NULL,
	memberserverimagedescription VARCHAR(255) NULL,
	memberserverimagestatusname VARCHAR(255) NOT NULL,
	memberserverimagestatus VARCHAR(255) NOT NULL,
	membersererimageoperation VARCHAR(255) NOT NULL,
	memberserverimageplatformtype VARCHAR(255) NOT NULL,
	createdate TIMESTAMP NOT NULL,
	memberserverimageblockstoragetotalrows INT8 NULL,
	memberserverimageblockstoragetotalsize INT8 NULL,
	CONSTRAINT memberserverimage_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS networkacl (
	id INTEGER NOT NULL DEFAULT NEXTVAL('networkacl_seq'),
	vpcid INT8 NOT NULL,
	vpcid_copy INT8 NULL,
	networkaclno VARCHAR(255) NOT NULL,
	networkaclname VARCHAR(255) NOT NULL,
	networkaclstatus VARCHAR(255) NOT NULL,
	networkacldescription VARCHAR(255) NULL,
	createdate TIMESTAMP NOT NULL,
	isdefault BOOL NOT NULL,
	CONSTRAINT networkacl_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS networkacldenyallowgroup (
	id INTEGER NOT NULL DEFAULT NEXTVAL('networkacldenyallowgroup_seq'),
	vpcid INT8 NOT NULL,
	vpcid_copy INT8 NULL,
	networkacldenyallowgroupno VARCHAR(255) NOT NULL,
	networkacldenyallowgroupname VARCHAR(255) NOT NULL,
	networkacldenyallowgroupstatus VARCHAR(255) NOT NULL,
	iplist JSONB NULL,
	networkacldenyallowgroupdescription VARCHAR(255) NULL,
	createdate TIMESTAMP NOT NULL,
	isapplied BOOL NOT NULL,
	CONSTRAINT networkacldenyallowgroup_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS networkaclrule (
	id INTEGER NOT NULL DEFAULT NEXTVAL('networkaclrule_seq'),
	networkaclid INT8 NOT NULL,
	networkaclid_copy INT8 NULL,
	protocolid INT8 NOT NULL,
	protocolid_copy INT8 NULL,
	priority INT8 NOT NULL,
	portrange VARCHAR(255) NULL,
	ruleaction VARCHAR(255) NOT NULL,
	createdate TIMESTAMP NOT NULL,
	ipblock VARCHAR(255) NULL,
	denyallowgroupno VARCHAR(255) NULL,
	networkaclruletype VARCHAR(255) NOT NULL,
	networkaclruledescription VARCHAR(255) NULL,
	CONSTRAINT networkaclrule_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS routetable (
	id INTEGER NOT NULL DEFAULT NEXTVAL('routetable_seq'),
	regionid INT8 NOT NULL,
	regionid_copy INT8 NULL,
	vpcid INT8 NOT NULL,
	vpcid_copy INT8 NULL,
	routetableno VARCHAR(255) NOT NULL,
	routetablename VARCHAR(255) NOT NULL,
	supportedsubnettype VARCHAR(255) NOT NULL,
	isdefault BOOL NOT NULL,
	routetablestatus VARCHAR(255) NOT NULL,
	routetabledescription VARCHAR(255) NULL,
	CONSTRAINT routetable_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS subnet (
	id INTEGER NOT NULL DEFAULT NEXTVAL('subnet_seq'),
	vpcid INT8 NOT NULL,
	vpcid_copy INT8 NULL,
	zoneid INT8 NOT NULL,
	zoneid_copy INT8 NULL,
	networkaclid INT8 NOT NULL,
	networkaclid_copy INT8 NULL,
	subnetno VARCHAR(255) NOT NULL,
	subnetname VARCHAR(255) NOT NULL,
	subnet VARCHAR(255) NOT NULL,
	subnetstatus VARCHAR(255) NOT NULL,
	createdate TIMESTAMP NULL,
	subnettype VARCHAR(255) NOT NULL,
	usagetype VARCHAR(255) NULL,
	networkaclno VARCHAR(255) NULL,
	CONSTRAINT subnet_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS autoscalinggroup (
	id INTEGER NOT NULL DEFAULT NEXTVAL('autoscalinggroup_seq'),
	vpcid INT8 NOT NULL,
	vpcid_copy INT8 NULL,
	subnetid INT8 NOT NULL,
	subnetid_copy INT8 NULL,
	servernameprefix VARCHAR(255) NULL,
	autoscalinggroupno VARCHAR(255) NOT NULL,
	autoscalinggroupname VARCHAR(255) NOT NULL,
	launchconfigurationno VARCHAR(255) NOT NULL,
	minsize INT8 NOT NULL,
	maxsize INT8 NOT NULL,
	desiredcapacity INT8 NOT NULL,
	defaultcooldown INT8 NOT NULL,
	healthcheckgraceperiod INT8 NOT NULL,
	healthchecktype VARCHAR(255) NOT NULL,
	createdate TIMESTAMP NOT NULL,
	autoscalinggroupstatus VARCHAR(255) NOT NULL,
	inautoscalinggroupserverinstancelist JSONB NULL,
	targetgroupnolist JSONB NULL,
	accesscontrolgroupnolist JSONB NOT NULL,
	suspendedprocesslist JSONB NULL,
	CONSTRAINT autoscalinggroup_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS loadbalancersubnet (
	id INTEGER NOT NULL DEFAULT NEXTVAL('loadbalancersubnet_seq'),
	zoneid INT8 NOT NULL,
	zoneid_copy INT8 NULL,
	subnetid INT8 NOT NULL,
	subnetid_copy INT8 NULL,
	publicipinstanceid INT8 NULL,
	publicipinstanceid_copy INT8 NULL,
	CONSTRAINT loadbalancersubnet_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS natgatewayinstance (
	id INTEGER NOT NULL DEFAULT NEXTVAL('natgatewayinstance_seq'),
	vpcid INT8 NOT NULL,
	vpcid_copy INT8 NULL,
	subnetid INT8 NOT NULL,
	subnetid_copy INT8 NULL,
	natgatewayinstanceno VARCHAR(255) NOT NULL,
	natgatewayname VARCHAR(255) NOT NULL,
	publicip VARCHAR(255) NULL,
	natgatewayinstancestatus VARCHAR(255) NOT NULL,
	natgatewayinstancestatusname VARCHAR(255) NOT NULL,
	natgatewayinstanceoperation VARCHAR(255) NOT NULL,
	createdate TIMESTAMP NOT NULL,
	natgatewaydescription VARCHAR(255) NULL,
	natgatewaytype VARCHAR(255) NULL,
	privateip VARCHAR(255) NULL,
	publicipinstanceno VARCHAR(255) NULL,
	CONSTRAINT natgatewayinstance_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS networkinterface (
	id INTEGER NOT NULL DEFAULT NEXTVAL('networkinterface_seq'),
	subnetid INT8 NOT NULL,
	subnetid_copy INT8 NULL,
	networkinterfaceno VARCHAR(255) NOT NULL,
	networkinterfacename VARCHAR(255) NOT NULL,
	deleteontermination BOOL NOT NULL,
	isdefault BOOL NOT NULL,
	devicename VARCHAR(255) NULL,
	networkinterfacestatus VARCHAR(255) NOT NULL,
	instancetype VARCHAR(255) NULL,
	instanceno VARCHAR(255) NULL,
	ip VARCHAR(255) NOT NULL,
	macaddress VARCHAR(255) NOT NULL,
	accesscontrolgroupnolist JSONB NULL,
	networkinterfacedescription VARCHAR(255) NULL,
	secondaryiplist JSONB NULL,
	CONSTRAINT networkinterface_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS route (
	id INTEGER NOT NULL DEFAULT NEXTVAL('route_seq'),
	subnetid INT8 NULL,
	subnetid_copy INT8 NULL,
	networkinterfaceno VARCHAR(255) NULL,
	networkinterfaceno_copy VARCHAR(255) NULL,
	routetableid INT8 NOT NULL,
	routetableid_copy INT8 NULL,
	destinationcidrblock VARCHAR(255) NOT NULL,
	targetname VARCHAR(255) NOT NULL,
	targettype VARCHAR(255) NOT NULL,
	targetno VARCHAR(255) NOT NULL,
	isdefault BOOL NOT NULL,
	CONSTRAINT route_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS scalingpolicy (
	id INTEGER NOT NULL DEFAULT NEXTVAL('scalingpolicy_seq'),
	autoscalinggroupid INT8 NOT NULL,
	autoscalinggroupid_copy INT8 NULL,
	policyno VARCHAR(255) NOT NULL,
	policyname VARCHAR(255) NOT NULL,
	adjustmenttype VARCHAR(255) NOT NULL,
	scalingadjustment INT8 NOT NULL,
	minadjustmentstep INT8 NULL,
	cooldown INT8 NULL,
	CONSTRAINT scalingpolicy_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS scheduledupdategroupaction (
	id INTEGER NOT NULL DEFAULT NEXTVAL('scheduledupdategroupaction_seq'),
	autoscalinggroupid INT8 NOT NULL,
	autoscalinggroupid_copy INT8 NULL,
	scheduledactionno VARCHAR(255) NOT NULL,
	scheduledactionname VARCHAR(255) NOT NULL,
	minsize INT8 NOT NULL,
	maxsize INT8 NOT NULL,
	desiredcapacity INT8 NOT NULL,
	starttime TIMESTAMP NOT NULL,
	endtime TIMESTAMP NULL,
	recurrence VARCHAR(255) NULL,
	timezone VARCHAR(255) NOT NULL,
	CONSTRAINT scheduledupdategroupaction_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS serverinstance (
	id INTEGER NOT NULL DEFAULT NEXTVAL('serverinstance_seq'),
	serverproductcodeid INT8 NOT NULL,
	serverproductcodeid_copy INT8 NULL,
	zoneid INT8 NOT NULL,
	zoneid_copy INT8 NULL,
	regionid INT8 NOT NULL,
	regionid_copy INT8 NULL,
	vpcid INT8 NOT NULL,
	vpcid_copy INT8 NULL,
	subnetid INT8 NOT NULL,
	subnetid_copy INT8 NULL,
	serverinstanceno VARCHAR(255) NOT NULL,
	servername VARCHAR(255) NOT NULL,
	serverdescription VARCHAR(255) NULL,
	cpucount INT8 NOT NULL,
	memorysize INT8 NOT NULL,
	platformtype VARCHAR(255) NOT NULL,
	loginkeyname VARCHAR(255) NOT NULL,
	publicipinstanceno VARCHAR(255) NULL,
	publicip VARCHAR(255) NULL,
	serverinstancestatus VARCHAR(255) NOT NULL,
	serverinstanceoperation VARCHAR(255) NOT NULL,
	serverinstancestatusname VARCHAR(255) NOT NULL,
	createdate TIMESTAMP NOT NULL,
	uptime TIMESTAMP NOT NULL,
	serverimageproductcode VARCHAR(255) NOT NULL,
	isprotectservertermination BOOL NOT NULL,
	networkinterfacenolist JSONB NOT NULL,
	initscriptno VARCHAR(255) NULL,
	serverinstancetype VARCHAR(255) NOT NULL,
	baseblockstoragedisktype VARCHAR(255) NOT NULL,
	baseblockstoragediskdetailtype VARCHAR(255) NOT NULL,
	placementgroupno VARCHAR(255) NULL,
	placementgroupname VARCHAR(255) NULL,
	memberserverimageinstanceno VARCHAR(255) NULL,
	blockdevicepartitionlist JSONB NULL,
	CONSTRAINT serverinstance_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE IF NOT EXISTS activitylog (
	id INTEGER NOT NULL DEFAULT NEXTVAL('activitylog_seq'),
	zoneid INT8 NOT NULL,
	zoneid_copy INT8 NULL,
	serverinstanceid INT8 NOT NULL,
	serverinstanceid_copy INT8 NULL,
	autoscalinggroupid INT8 NOT NULL,
	autoscalinggroupid_copy INT8 NULL,
	activityno VARCHAR(255) NOT NULL,
	zonecode VARCHAR(255) NULL,
	actionname VARCHAR(255) NOT NULL,
	actionstatus VARCHAR(255) NOT NULL,
	actioncause VARCHAR(255) NULL,
	actiondescription VARCHAR(255) NOT NULL,
	starttime TIMESTAMP NOT NULL,
	endtime TIMESTAMP NULL,
	CONSTRAINT activitylog_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE targetgroup (
	id INTEGER NOT NULL DEFAULT NEXTVAL ('targetgroup_seq'),
    targetGroupNo VARCHAR(255) NOT NULL,
    targetGroupName VARCHAR(255) NOT NULL,
    targetType VARCHAR(255) NOT NULL,
    vpcid INT8 NOT NULL,
    vpcid_copy INT8 NULL,
    targetGroupProtocolType VARCHAR(255) NOT NULL,
    targetGroupPort VARCHAR(255) NOT NULL,
    targetGroupDescription VARCHAR(255) NULL,
    useStickySession BOOL NOT NULL,
    useProxyProtocol BOOL NOT NULL,
    algorithmType VARCHAR(255) NOT NULL,
    createDate TIMESTAMP NOT NULL,
    regionid INT8 NOT NULL,
    regionid_copy INT8 NULL,
    loadBalancerInstanceNo VARCHAR(255) NULL,
    healthCheckProtocolType VARCHAR(255) NOT NULL,
    healthCheckPort VARCHAR(255) NOT NULL,
    healthCheckUrlPath VARCHAR(255) NULL,
    healthCheckHttpMethodType VARCHAR(255) NULL,
    healthCheckCycle VARCHAR(255) NOT NULL,
    healthCheckUpThreshold VARCHAR(255) NOT NULL,
    healthCheckDownThreshold VARCHAR(255) NOT NULL,
    targetNoList VARCHAR(255) NULL,
	CONSTRAINT targetgroup_pkey PRIMARY KEY (id ASC)
);