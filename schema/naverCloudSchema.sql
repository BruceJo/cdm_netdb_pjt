--- recovery details
DROP TABLE IF EXISTS accesscontrolgroup;
DROP TABLE IF EXISTS adjustmenttype;
DROP TABLE IF EXISTS inautoscalinggroupserverinstance;
DROP TABLE IF EXISTS initscript;
DROP TABLE IF EXISTS loadbalancerruleaction;
DROP TABLE IF EXISTS loadbalancerrulecondition;
DROP TABLE IF EXISTS loginkey;
DROP TABLE IF EXISTS memberserverimageinstance;
DROP TABLE IF EXISTS placementgroup;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS protocoltype;
DROP TABLE IF EXISTS publicipinstance;
DROP TABLE IF EXISTS region;
DROP TABLE IF EXISTS accesscontrolgrouprule;
DROP TABLE IF EXISTS launchconfiguration;
DROP TABLE IF EXISTS vpc;
DROP TABLE IF EXISTS vpcpeeringinstance;
DROP TABLE IF EXISTS zone;
DROP TABLE IF EXISTS blockstorageinstance;
DROP TABLE IF EXISTS blockstoragesnapshotinstance;
DROP TABLE IF EXISTS loadbalancerinstance;
DROP TABLE IF EXISTS loadbalancerlistener;
DROP TABLE IF EXISTS loadbalancerrule;
DROP TABLE IF EXISTS memberserverimage;
DROP TABLE IF EXISTS networkacl;
DROP TABLE IF EXISTS networkacldenyallowgroup;
DROP TABLE IF EXISTS networkaclrule;
DROP TABLE IF EXISTS routetable;
DROP TABLE IF EXISTS subnet;
DROP TABLE IF EXISTS autoscalinggroup;
DROP TABLE IF EXISTS loadbalancersubnet;
DROP TABLE IF EXISTS natgatewayinstance;
DROP TABLE IF EXISTS networkinterface;
DROP TABLE IF EXISTS route;
DROP TABLE IF EXISTS scalingpolicy;
DROP TABLE IF EXISTS scheduledupdategroupaction;
DROP TABLE IF EXISTS serverinstance;
DROP TABLE IF EXISTS activitylog;

DROP TABLE IF EXISTS recoveryplan;
DROP TABLE IF EXISTS recoveryresults;

DROP SEQUENCE IF EXISTS accesscontrolgroup_seq;
DROP SEQUENCE IF EXISTS adjustmenttype_seq;
DROP SEQUENCE IF EXISTS inautoscalinggroupserverinstance_seq;
DROP SEQUENCE IF EXISTS initscript_seq;
DROP SEQUENCE IF EXISTS loadbalancerruleaction_seq;
DROP SEQUENCE IF EXISTS loadbalancerrulecondition_seq;
DROP SEQUENCE IF EXISTS loginkey_seq;
DROP SEQUENCE IF EXISTS memberserverimageinstance_seq;
DROP SEQUENCE IF EXISTS placementgroup_seq;
DROP SEQUENCE IF EXISTS product_seq;
DROP SEQUENCE IF EXISTS protocoltype_seq;
DROP SEQUENCE IF EXISTS publicipinstance_seq;
DROP SEQUENCE IF EXISTS region_seq;
DROP SEQUENCE IF EXISTS accesscontrolgrouprule_seq;
DROP SEQUENCE IF EXISTS launchconfiguration_seq;
DROP SEQUENCE IF EXISTS vpc_seq;
DROP SEQUENCE IF EXISTS vpcpeeringinstance_seq;
DROP SEQUENCE IF EXISTS zone_seq;
DROP SEQUENCE IF EXISTS blockstorageinstance_seq;
DROP SEQUENCE IF EXISTS blockstoragesnapshotinstance_seq;
DROP SEQUENCE IF EXISTS loadbalancerinstance_seq;
DROP SEQUENCE IF EXISTS loadbalancerlistener_seq;
DROP SEQUENCE IF EXISTS loadbalancerrule_seq;
DROP SEQUENCE IF EXISTS memberserverimage_seq;
DROP SEQUENCE IF EXISTS networkacl_seq;
DROP SEQUENCE IF EXISTS networkacldenyallowgroup_seq;
DROP SEQUENCE IF EXISTS networkaclrule_seq;
DROP SEQUENCE IF EXISTS routetable_seq;
DROP SEQUENCE IF EXISTS subnet_seq;
DROP SEQUENCE IF EXISTS autoscalinggroup_seq;
DROP SEQUENCE IF EXISTS loadbalancersubnet_seq;
DROP SEQUENCE IF EXISTS natgatewayinstance_seq;
DROP SEQUENCE IF EXISTS networkinterface_seq;
DROP SEQUENCE IF EXISTS route_seq;
DROP SEQUENCE IF EXISTS scalingpolicy_seq;
DROP SEQUENCE IF EXISTS scheduledupdategroupaction_seq;
DROP SEQUENCE IF EXISTS serverinstance_seq;
DROP SEQUENCE IF EXISTS activitylog_seq;

DROP SEQUENCE IF EXISTS recoveryplan_seq;
DROP SEQUENCE IF EXISTS recoveryresults_seq;

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

CREATE SEQUENCE IF NOT EXISTS recoveryplan_seq;
CREATE SEQUENCE IF NOT EXISTS recoveryresults_seq;

CREATE TABLE IF NOT EXISTS accesscontrolgroup (
	id INTEGER NOT NULL DEFAULT NEXTVAL('accesscontrolgroup_seq'),
	accesscontrolgroupno VARCHAR(255) NOT NULL,
	accesscontrolgroupname VARCHAR(255) NOT NULL,
	isdefault BOOL NOT NULL,
	vpcno VARCHAR(255) NOT NULL,
	accesscontrolgroupstatus VARCHAR(255) NOT NULL,
	accesscontrolgroupdescription VARCHAR(255) NULL,
	CONSTRAINT accesscontrolgroup_pkey PRIMARY KEY (id ASC),
    CONSTRAINT accesscontrolgroup_ukey UNIQUE (accesscontrolgroupno, vpcno)
);

CREATE TABLE IF NOT EXISTS adjustmenttype (
	id INTEGER NOT NULL DEFAULT NEXTVAL('adjustmenttype_seq'),
	code VARCHAR(255) NOT NULL,
	codename VARCHAR(255) NOT NULL,
	CONSTRAINT adjustmenttype_pkey PRIMARY KEY (id ASC),
    CONSTRAINT adjustmenttype_ukey UNIQUE (code, codename)
);



CREATE TABLE IF NOT EXISTS inautoscalinggroupserverinstance (
	id INTEGER NOT NULL DEFAULT NEXTVAL('inautoscalinggroupserverinstance_seq'),
	serverinstanceno VARCHAR(255) NULL,
	healthstatus VARCHAR(255) NULL,
	lifecyclestate VARCHAR(255) NULL,
	CONSTRAINT inautoscalinggroupserverinstance_pkey PRIMARY KEY (id ASC),
    CONSTRAINT inautoscalinggroupserverinstance_ukey UNIQUE (serverinstanceno, healthstatus, lifecyclestate)	-- PKEY 가 아니라 UKEY 로 변경
);


CREATE TABLE IF NOT EXISTS initscript (
	id INTEGER NOT NULL DEFAULT NEXTVAL('initscript_seq'),
	initscriptno VARCHAR(255) NOT NULL,
	initscriptname VARCHAR(255) NOT NULL,
	createdate TIMESTAMP NOT NULL,
	initscriptdescription VARCHAR(255) NULL,
	initscriptcontent STRING NOT NULL,
	ostype VARCHAR(255) NOT NULL,
	CONSTRAINT initscript_pkey PRIMARY KEY (id ASC),
    CONSTRAINT initscript_ukey UNIQUE (initscriptno)
);


CREATE TABLE IF NOT EXISTS loadbalancerruleaction (
	id INTEGER NOT NULL DEFAULT NEXTVAL('loadbalancerruleaction_seq'),
	ruleactiontype VARCHAR(255) NOT NULL,
	targetgroupaction VARCHAR(255) NULL,
	redirectionaction VARCHAR(255) NULL,
	CONSTRAINT loadbalancerruleaction_pkey PRIMARY KEY (id ASC),
    CONSTRAINT loadbalancerruleaction_ukey UNIQUE (ruleactiontype, targetgroupaction, redirectionaction)
);


CREATE TABLE IF NOT EXISTS loadbalancerrulecondition (
	id INTEGER NOT NULL DEFAULT NEXTVAL('loadbalancerrulecondition_seq'),
	ruleconditiontype VARCHAR(255) NOT NULL,
	hostheadercondition VARCHAR(255) NULL,
	pathpatterncondition VARCHAR(255) NULL,
	CONSTRAINT loadbalancerrulecondition_pkey PRIMARY KEY (id ASC),
    CONSTRAINT loadbalancerrulecondition_ukey UNIQUE (ruleconditiontype, hostheadercondition, pathpatterncondition)
);


CREATE TABLE IF NOT EXISTS loginkey (
	id INTEGER NOT NULL DEFAULT NEXTVAL('loginkey_seq'),
	fingerprint VARCHAR(255) NOT NULL,
	keyname VARCHAR(255) NOT NULL,
	createdate TIMESTAMP NOT NULL,
	CONSTRAINT loginkey_pkey PRIMARY KEY (id ASC),
    CONSTRAINT loginkey_ukey UNIQUE (fingerprint, keyname, createdate)
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
	sharedloginidlist JSONB NOT NULL, -- LIST 구조는 JSONB 형식으로 INSERT
	CONSTRAINT memberserverimageinstance_pkey PRIMARY KEY (id ASC),
    CONSTRAINT memberserverimageinstance_ukey UNIQUE (memberserverimageinstanceno)
);

CREATE TABLE IF NOT EXISTS placementgroup (
	id INTEGER NOT NULL DEFAULT NEXTVAL('placementgroup_seq'),
	placementgroupno VARCHAR(255) NOT NULL,
	placementgroupname VARCHAR(255) NOT NULL,
	placementgrouptype VARCHAR(255) NOT NULL,
	CONSTRAINT placementgroup_pkey PRIMARY KEY (id ASC),
    CONSTRAINT placementgroup_ukey UNIQUE (placementgroupno)
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
	CONSTRAINT product_pkey PRIMARY KEY (id ASC),
    CONSTRAINT product_ukey UNIQUE (productcode)	-- PKEY 가 아니라 UKEY 로 변경
);


CREATE TABLE IF NOT EXISTS protocoltype (
	id INTEGER NOT NULL DEFAULT NEXTVAL('protocoltype_seq'),
	code VARCHAR(255) NOT NULL,
	codename VARCHAR(255) NOT NULL,
	codenumber INT8 NOT NULL,
	CONSTRAINT protocoltype_pkey PRIMARY KEY (id ASC),
    CONSTRAINT protocoltype_ukey UNIQUE (codenumber)
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
	CONSTRAINT publicipinstance_pkey PRIMARY KEY (id ASC),
    CONSTRAINT publicipinstance_ukey UNIQUE (publicipinstanceno)
);

CREATE TABLE IF NOT EXISTS region (
	id INTEGER NOT NULL DEFAULT NEXTVAL('region_seq'),
	regioncode VARCHAR(255) NOT NULL,
	regionname VARCHAR(255) NOT NULL,
	CONSTRAINT region_pkey PRIMARY KEY (id ASC),
    CONSTRAINT region_ukey UNIQUE (regioncode)
);

CREATE TABLE IF NOT EXISTS accesscontrolgrouprule (
	id INTEGER NOT NULL DEFAULT NEXTVAL('accesscontrolgrouprule_seq'),
	accesscontrolgroupid INT8 NOT NULL,
	protocoltypeid INT8 NOT NULL,
	ipblock VARCHAR(255) NULL,
	accesscontrolgroupsequence VARCHAR(255) NULL,
	portrange VARCHAR(255) NULL,
	accesscontrolgroupruletype VARCHAR(255) NOT NULL,
	accesscontrolgroupruledescription VARCHAR(255) NOT NULL,
	CONSTRAINT accesscontrolgrouprule_pkey PRIMARY KEY (id ASC),
    CONSTRAINT accesscontrolgrouprule_ukey UNIQUE (accesscontrolgroupid),
	CONSTRAINT accesscontrolgrouprule_accesscontrolgroupid_fkey FOREIGN KEY (accesscontrolgroupid) REFERENCES accesscontrolgroup(id),
	CONSTRAINT accesscontrolgrouprule_protocoltypeid_fkey FOREIGN KEY (protocoltypeid) REFERENCES protocoltype(id)
);

CREATE TABLE IF NOT EXISTS launchconfiguration (
	id INTEGER NOT NULL DEFAULT NEXTVAL('launchconfiguration_seq'),
	regionid INT8 NOT NULL,
	serverproductid INT8 NOT NULL,
	loginkeyid INT8 NOT NULL,
	launchconfigurationno VARCHAR(255) NOT NULL,
	launchconfigurationname VARCHAR(255) NOT NULL,
	serverimageproductcode VARCHAR(255) NULL,
	memberserverimageinstanceno VARCHAR(255) NULL,
	createdate DATE NOT NULL,
	launchconfigurationstatus VARCHAR(255) NOT NULL,
	initscriptno VARCHAR(255) NULL,
	isencryptedvolume BOOL NOT NULL,
	CONSTRAINT launchconfiguration_pkey PRIMARY KEY (id ASC),
    CONSTRAINT launchconfiguration_ukey UNIQUE (regionid, launchconfigurationno),
	CONSTRAINT launchconfiguration_regionid_fkey FOREIGN KEY (regionid) REFERENCES region(id),
	CONSTRAINT launchconfiguration_serverproductid_fkey FOREIGN KEY (serverproductid) REFERENCES product(id),
	CONSTRAINT launchconfiguration_loginkeyid_fkey FOREIGN KEY (loginkeyid) REFERENCES loginkey(id)
);

CREATE TABLE IF NOT EXISTS vpc (
	id INTEGER NOT NULL DEFAULT NEXTVAL('vpc_seq'),
	regionid INT8 NOT NULL,
	vpcno VARCHAR(255) NOT NULL,
	vpcname VARCHAR(255) NOT NULL,
	ipv4cidrblock VARCHAR(255) NOT NULL,
	vpcstatus VARCHAR(255) NOT NULL,
	createdate TIMESTAMP NOT NULL,
	CONSTRAINT vpc_pkey PRIMARY KEY (id ASC),
    CONSTRAINT vpc_ukey UNIQUE (regionid, vpcno),
	CONSTRAINT vpc_regionid_fkey FOREIGN KEY (regionid) REFERENCES region(id)
);

CREATE TABLE IF NOT EXISTS vpcpeeringinstance (
	id INTEGER NOT NULL DEFAULT NEXTVAL('vpcpeeringinstance_seq'),
	regionid INT8 NOT NULL,
	sourcevpcid INT8 NOT NULL,
	targetvpcid INT8 NOT NULL,
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
	CONSTRAINT vpcpeeringinstance_pkey PRIMARY KEY (id ASC),
    CONSTRAINT vpcpeeringinstance_ukey UNIQUE (regionid, vpcpeeringinstanceno),
	CONSTRAINT vpcpeeringinstance_regionid_fkey FOREIGN KEY (regionid) REFERENCES region(id),
	CONSTRAINT vpcpeeringinstance_sourcevpcid_fkey FOREIGN KEY (sourcevpcid) REFERENCES vpc(id),
	CONSTRAINT vpcpeeringinstance_targetvpcid_fkey FOREIGN KEY (targetvpcid) REFERENCES vpc(id)
);

CREATE TABLE IF NOT EXISTS zone (
	id INTEGER NOT NULL DEFAULT NEXTVAL('zone_seq'),
	regionid INT8 NOT NULL,
	zonename VARCHAR(255) NOT NULL,
	zonecode VARCHAR(255) NOT NULL,
	zonedescription VARCHAR(255) NOT NULL,
	CONSTRAINT zone_pkey PRIMARY KEY (id ASC),
    CONSTRAINT zone_ukey UNIQUE (regionid, zonecode),
	CONSTRAINT zone_regionid_fkey FOREIGN KEY (regionid) REFERENCES region(id)
);


CREATE TABLE IF NOT EXISTS blockstorageinstance (
	id INTEGER NOT NULL DEFAULT NEXTVAL('blockstorageinstance_seq'),
	zoneid INT8 NOT NULL,
	regionid INT8 NOT NULL,
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
	CONSTRAINT blockstorageinstance_pkey PRIMARY KEY (id ASC),
    CONSTRAINT blockstorageinstance_ukey UNIQUE (regionid, zoneid, blockstorageinstanceno),
	CONSTRAINT blockstorageinstance_zoneid_fkey FOREIGN KEY (zoneid) REFERENCES zone(id),
	CONSTRAINT blockstorageinstance_regionid_fkey FOREIGN KEY (regionid) REFERENCES region(id)
);

CREATE TABLE IF NOT EXISTS blockstoragesnapshotinstance (
	id INTEGER NOT NULL DEFAULT NEXTVAL('blockstoragesnapshotinstance_seq'),
	blockstorageinstanceid INT8 NOT NULL,
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
	CONSTRAINT blockstoragesnapshotinstance_pkey PRIMARY KEY (id ASC),
    CONSTRAINT blockstoragesnapshotinstance_ukey UNIQUE (blockstorageinstanceid, blockstoragesnapshotinstanceno),
	CONSTRAINT blockstoragesnapshotinstance_blockstoragenstanceid_fkey FOREIGN KEY (blockstorageinstanceid) REFERENCES blockstorageinstance(id)
);

CREATE TABLE IF NOT EXISTS loadbalancerinstance (
	id INTEGER NOT NULL DEFAULT NEXTVAL('loadbalancerinstance_seq'),
	vpcid INT8 NOT NULL,
	regionid INT8 NOT NULL,
	loadbalancerinstanceno VARCHAR(255) NOT NULL,
	loadbalancerinstancestatus VARCHAR(255) NOT NULL,
	loadbalancerinstanceoperation VARCHAR(255) NOT NULL,
	loadbalancerinstancestatusname VARCHAR(255) NOT NULL,
	loadbalancerdescription STRING NULL,
	createdate TIMESTAMP NOT NULL,
	loadbalancername VARCHAR(255) NOT NULL,
	loadbalancerdomain VARCHAR(255) NOT NULL,
	loadbalanceriplist JSONB NULL, 	-- LIST 구조는 JSONB 형식으로 INSERT
	loadbalancertype VARCHAR(255) NOT NULL,
	loadbalancernetworktype VARCHAR(255) NOT NULL,
	throughputtype VARCHAR(255) NOT NULL,
	idletimeout INT8 NULL,
	subnetnolist JSONB NOT NULL, 	-- LIST 구조는 JSONB 형식으로 INSERT
	loadbalancersubnetlist JSONB NOT NULL, 	-- LIST 구조는 JSONB 형식으로 INSERT
	loadbalancerlistenernolist JSONB NULL, 	-- LIST 구조는 JSONB 형식으로 INSERT
	CONSTRAINT loadbalancerinstance_pkey PRIMARY KEY (id ASC),
    CONSTRAINT loadbalancerinstance_ukey UNIQUE (vpcid, regionid, loadbalancerinstanceno),
	CONSTRAINT loadbalancerinstance_vpcid_fkey FOREIGN KEY (vpcid) REFERENCES vpc(id),
	CONSTRAINT loadbalancerinstance_regionid_fkey FOREIGN KEY (regionid) REFERENCES region(id)
);

CREATE TABLE IF NOT EXISTS loadbalancerlistener (
	id INTEGER NOT NULL DEFAULT NEXTVAL('loadbalancerlistener_seq'),
	loadbalancerinstanceid INT8 NOT NULL,
	loadbalancerlistenerno VARCHAR(255) NOT NULL,
	protocoltype VARCHAR(50) NOT NULL,
	port INT8 NOT NULL,
	usehttp2 BOOL NOT NULL,
	sslcertificateno VARCHAR(255) NULL,
	tlsminversiontype VARCHAR(50) NULL,
	loadbalancerrulenolist JSONB NOT NULL,	-- LIST 구조는 JSONB 형식으로 INSERT
	ciphersuitelist JSONB NOT NULL,			-- LIST 구조는 JSONB 형식으로 INSERT
	CONSTRAINT loadbalancerlistener_pkey PRIMARY KEY (id ASC),
    CONSTRAINT loadbalancerlistener_ukey UNIQUE (loadbalancerinstanceid, loadbalancerlistenerno),
	CONSTRAINT loadbalancerlistener_loadbalancerinstanceid_fkey FOREIGN KEY (loadbalancerinstanceid) REFERENCES loadbalancerinstance(id)
);


CREATE TABLE IF NOT EXISTS loadbalancerrule (
	id INTEGER NOT NULL DEFAULT NEXTVAL('loadbalancerrule_seq'),
	loadbalancerlistenerid INT8 NOT NULL,
	loadbalancerruleno VARCHAR(255) NOT NULL,
	priority INT8 NOT NULL,
	loadbalancerruleconditionlist JSONB NOT NULL,	-- LIST 구조는 JSONB 형식으로 INSERT
	loadbalancerruleactionlist JSONB NOT NULL,		-- LIST 구조는 JSONB 형식으로 INSERT
	CONSTRAINT loadbalancerrule_pkey PRIMARY KEY (id ASC),
    CONSTRAINT loadbalancerrule_ukey UNIQUE (loadbalancerlistenerid, loadbalancerruleno),
	CONSTRAINT loadbalancerrule_loadbalancerlistenerid_fkey FOREIGN KEY (loadbalancerlistenerid) REFERENCES loadbalancerlistener(id)
);


CREATE TABLE IF NOT EXISTS memberserverimage (
	id INTEGER NOT NULL DEFAULT NEXTVAL('memberserverimage_seq'),
	originalserverinstanceid INT8 NOT NULL,
	zoneid INT8 NOT NULL,
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
	CONSTRAINT memberserverimage_pkey PRIMARY KEY (id ASC),
    CONSTRAINT memberserverimage_ukey UNIQUE (zoneid, memberserverimageno),
	CONSTRAINT memberserverimage_zoneid_fkey FOREIGN KEY (zoneid) REFERENCES zone(id)
);

CREATE TABLE IF NOT EXISTS networkacl (
	id INTEGER NOT NULL DEFAULT NEXTVAL('networkacl_seq'),
	vpcid INT8 NOT NULL,
	networkaclno VARCHAR(255) NOT NULL,
	networkaclname VARCHAR(255) NOT NULL,
	networkaclstatus VARCHAR(255) NOT NULL,
	networkacldescription VARCHAR(255) NULL,
	createdate TIMESTAMP NOT NULL,
	isdefault BOOL NOT NULL,
	CONSTRAINT networkacl_pkey PRIMARY KEY (id ASC),
    CONSTRAINT networkacl_ukey UNIQUE (vpcid, networkaclno),
	CONSTRAINT networkacl_vpcid_fkey FOREIGN KEY (vpcid) REFERENCES vpc(id)
);

CREATE TABLE IF NOT EXISTS networkacldenyallowgroup (
	id INTEGER NOT NULL DEFAULT NEXTVAL('networkacldenyallowgroup_seq'),
	vpcid INT8 NOT NULL,
	networkacldenyallowgroupno VARCHAR(255) NOT NULL,
	networkacldenyallowgroupname VARCHAR(255) NOT NULL,
	networkacldenyallowgroupstatus VARCHAR(255) NOT NULL,
	iplist JSONB NULL,	-- LIST 구조는 JSONB 형식으로 INSERT
	networkacldenyallowgroupdescription VARCHAR(255) NULL,
	createdate TIMESTAMP NOT NULL,
	isapplied BOOL NOT NULL,
	CONSTRAINT networkacldenyallowgroup_pkey PRIMARY KEY (id ASC),
    CONSTRAINT networkacldenyallowgroup_ukey UNIQUE (vpcid, networkacldenyallowgroupno),
	CONSTRAINT networkacldenyallowgroup_vpcid_fkey FOREIGN KEY (vpcid) REFERENCES vpc(id)
);

CREATE TABLE IF NOT EXISTS networkaclrule (
	id INTEGER NOT NULL DEFAULT NEXTVAL('networkaclrule_seq'),
	networkaclid INT8 NOT NULL,
	protocolid INT8 NOT NULL,
	priority INT8 NOT NULL,
	portrange VARCHAR(255) NULL,
	ruleaction VARCHAR(255) NOT NULL,
	createdate TIMESTAMP NOT NULL,
	ipblock VARCHAR(255) NULL,
	denyallowgroupno VARCHAR(255) NULL,
	networkaclruletype VARCHAR(255) NOT NULL,
	networkaclruledescription VARCHAR(255) NULL,
	CONSTRAINT networkaclrule_pkey PRIMARY KEY (id ASC),
    CONSTRAINT networkaclrule_ukey UNIQUE (networkaclid, protocolid, priority, portrange, ruleaction, ipblock, networkaclruletype),
	CONSTRAINT networkaclrule_networkaclid_fkey FOREIGN KEY (networkaclid) REFERENCES networkacl(id),
	CONSTRAINT networkaclrule_protocolid_fkey FOREIGN KEY (protocolid) REFERENCES protocoltype(id)
);

CREATE TABLE IF NOT EXISTS routetable (
	id INTEGER NOT NULL DEFAULT NEXTVAL('routetable_seq'),
	regionid INT8 NOT NULL,
	vpcid INT8 NOT NULL,
	routetableno VARCHAR(255) NOT NULL,
	routetablename VARCHAR(255) NOT NULL,
	supportedsubnettype VARCHAR(255) NOT NULL,
	isdefault BOOL NOT NULL,
	routetablestatus VARCHAR(255) NOT NULL,
	routetabledescription VARCHAR(255) NULL,
	CONSTRAINT routetable_pkey PRIMARY KEY (id ASC),
    CONSTRAINT routetable_ukey UNIQUE (regionid, vpcid, routetableno),
	CONSTRAINT routetable_regionid_fkey FOREIGN KEY (regionid) REFERENCES region(id),
	CONSTRAINT routetable_vpcid_fkey FOREIGN KEY (vpcid) REFERENCES vpc(id)
);

CREATE TABLE IF NOT EXISTS subnet (
	id INTEGER NOT NULL DEFAULT NEXTVAL('subnet_seq'),
	vpcid INT8 NOT NULL,
	zoneid INT8 NOT NULL,
	networkaclid INT8 NOT NULL,
	subnetno VARCHAR(255) NOT NULL,
	subnetname VARCHAR(255) NOT NULL,
	subnet VARCHAR(255) NOT NULL,
	subnetstatus VARCHAR(255) NOT NULL,
	createdate TIMESTAMP NULL,
	subnettype VARCHAR(255) NOT NULL,
	usagetype VARCHAR(255) NULL,
	networkaclno VARCHAR(255) NULL,
	CONSTRAINT subnet_pkey PRIMARY KEY (id ASC),
    CONSTRAINT subnet_ukey UNIQUE (vpcid, zoneid, networkaclid, subnetno),
	CONSTRAINT subnet_vpcid_fkey FOREIGN KEY (vpcid) REFERENCES vpc(id),
	CONSTRAINT subnet_zoneid_fkey FOREIGN KEY (zoneid) REFERENCES zone(id),
	CONSTRAINT subnet_networkaclid_fkey FOREIGN KEY (networkaclid) REFERENCES networkacl(id)
);

CREATE TABLE IF NOT EXISTS autoscalinggroup (
	id INTEGER NOT NULL DEFAULT NEXTVAL('autoscalinggroup_seq'),
	vpcid INT8 NOT NULL,
	subnetid INT8 NOT NULL,
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
	inautoscalinggroupserverinstancelist JSONB NULL,	-- LIST 구조는 JSONB 형식으로 INSERT
	targetgroupnolist JSONB NULL,						-- LIST 구조는 JSONB 형식으로 INSERT
	accesscontrolgroupnolist JSONB NOT NULL,			-- LIST 구조는 JSONB 형식으로 INSERT
	suspendedprocesslist JSONB NULL,					-- LIST 구조는 JSONB 형식으로 INSERT
	CONSTRAINT autoscalinggroup_pkey PRIMARY KEY (id ASC),
    CONSTRAINT autoscalinggroup_ukey UNIQUE (vpcid, subnetid, autoscalinggroupno),
	CONSTRAINT autoscalinggroup_vpcid_fkey FOREIGN KEY (vpcid) REFERENCES vpc(id),
	CONSTRAINT autoscalinggroup_subnetid_fkey FOREIGN KEY (subnetid) REFERENCES subnet(id)
);

CREATE TABLE IF NOT EXISTS loadbalancersubnet (
	id INTEGER NOT NULL DEFAULT NEXTVAL('loadbalancersubnet_seq'),
	zoneid INT8 NOT NULL,
	subnetid INT8 NOT NULL,
	publicipinstanceid INT8 NULL,
	CONSTRAINT loadbalancersubnet_pkey PRIMARY KEY (id ASC),
    CONSTRAINT loadbalancersubnet_ukey UNIQUE (zoneid, subnetid, publicipinstanceid),
	CONSTRAINT loadbalancersubnet_zoneid_fkey FOREIGN KEY (zoneid) REFERENCES zone(id),
	CONSTRAINT loadbalancersubnet_subnetid_fkey FOREIGN KEY (subnetid) REFERENCES subnet(id),
	CONSTRAINT loadbalancersubnet_publicipinstanceid_fkey FOREIGN KEY (publicipinstanceid) REFERENCES publicipinstance(id)
);


CREATE TABLE IF NOT EXISTS natgatewayinstance (
	id INTEGER NOT NULL DEFAULT NEXTVAL('natgatewayinstance_seq'),
	vpcid INT8 NOT NULL,
	subnetid INT8 NOT NULL,
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
	CONSTRAINT natgatewayinstance_pkey PRIMARY KEY (id ASC),
    CONSTRAINT loadbalancersubnet_ukey UNIQUE (vpcid, subnetid, natgatewayinstanceno),
	CONSTRAINT natgatewayinstance_vpcid_fkey FOREIGN KEY (vpcid) REFERENCES vpc(id),
	CONSTRAINT natgatewayinstance_subnetid_fkey FOREIGN KEY (subnetid) REFERENCES subnet(id)
);

CREATE TABLE IF NOT EXISTS networkinterface (
	id INTEGER NOT NULL DEFAULT NEXTVAL('networkinterface_seq'),
	subnetid INT8 NOT NULL,
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
	accesscontrolgroupnolist JSONB NULL,			-- LIST 구조는 JSONB 형식으로 INSERT
	networkinterfacedescription VARCHAR(255) NULL,
	secondaryiplist JSONB NULL,						-- LIST 구조는 JSONB 형식으로 INSERT
	CONSTRAINT networkinterface_pkey PRIMARY KEY (id ASC),
    CONSTRAINT networkinterface_ukey UNIQUE (subnetid, networkinterfaceno),
	CONSTRAINT networkinterface_subnetid_fkey FOREIGN KEY (subnetid) REFERENCES subnet(id)
);


CREATE TABLE IF NOT EXISTS route (
	id INTEGER NOT NULL DEFAULT NEXTVAL('route_seq'),
	subnetid INT8 NOT NULL,						-- 추가된 부분
	networkinterfaceno VARCHAR(255) NOT NULL, 	-- 추가된 부분
	routetableid INT8 NOT NULL,
	destinationcidrblock VARCHAR(255) NOT NULL,
	targetname VARCHAR(255) NOT NULL,
	targettype VARCHAR(255) NOT NULL,
	targetno VARCHAR(255) NOT NULL,
	isdefault BOOL NOT NULL,
	CONSTRAINT route_pkey PRIMARY KEY (id ASC),
    CONSTRAINT route_ukey UNIQUE (subnetid, networkinterfaceno),	-- 위의 UNIQUE 한 정보가 없어서 추가함.
	CONSTRAINT route_routetableid_fkey FOREIGN KEY (routetableid) REFERENCES routetable(id)
);

CREATE TABLE IF NOT EXISTS scalingpolicy (
	id INTEGER NOT NULL DEFAULT NEXTVAL('scalingpolicy_seq'),
	autoscalinggroupid INT8 NOT NULL,
	policyno VARCHAR(255) NOT NULL,
	policyname VARCHAR(255) NOT NULL,
	adjustmenttype VARCHAR(255) NOT NULL,
	scalingadjustment INT8 NOT NULL,
	minadjustmentstep INT8 NULL,
	cooldown INT8 NULL,
	CONSTRAINT scalingpolicy_pkey PRIMARY KEY (id ASC),
    CONSTRAINT scalingpolicy_ukey UNIQUE (autoscalinggroupid, policyno),
	CONSTRAINT scalingpolicy_autoscalinggroupid_fkey FOREIGN KEY (autoscalinggroupid) REFERENCES autoscalinggroup(id)
);

CREATE TABLE IF NOT EXISTS scheduledupdategroupaction (
	id INTEGER NOT NULL DEFAULT NEXTVAL('scheduledupdategroupaction_seq'),
	autoscalinggroupid INT8 NOT NULL,
	scheduledactionno VARCHAR(255) NOT NULL,
	scheduledactionname VARCHAR(255) NOT NULL,
	minsize INT8 NOT NULL,
	maxsize INT8 NOT NULL,
	desiredcapacity INT8 NOT NULL,
	starttime TIMESTAMP NOT NULL,
	endtime TIMESTAMP NULL,
	recurrence VARCHAR(255) NULL,
	timezone VARCHAR(255) NOT NULL,
	CONSTRAINT scheduledupdategroupaction_pkey PRIMARY KEY (id ASC),
    CONSTRAINT scheduledupdategroupaction_ukey UNIQUE (autoscalinggroupid, scheduledactionno),
	CONSTRAINT scheduledupdategroupaction_autoscalinggroupid_fkey FOREIGN KEY (autoscalinggroupid) REFERENCES autoscalinggroup(id)
);

CREATE TABLE IF NOT EXISTS serverinstance (
	id INTEGER NOT NULL DEFAULT NEXTVAL('serverinstance_seq'),
	serverproductcodeid INT8 NOT NULL,
	zoneid INT8 NOT NULL,
	regionid INT8 NOT NULL,
	vpcid INT8 NOT NULL,
	subnetid INT8 NOT NULL,
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
	networkinterfacenolist JSONB NOT NULL,	-- LIST 구조는 JSONB 형식으로 INSERT
	initscriptno VARCHAR(255) NULL,
	serverinstancetype VARCHAR(255) NOT NULL,
	baseblockstoragedisktype VARCHAR(255) NOT NULL,
	baseblockstoragediskdetailtype VARCHAR(255) NOT NULL,
	placementgroupno VARCHAR(255) NULL,
	placementgroupname VARCHAR(255) NULL,
	memberserverimageinstanceno VARCHAR(255) NULL,
	blockdevicepartitionlist JSONB NULL,	-- LIST 구조는 JSONB 형식으로 INSERT
	CONSTRAINT serverinstance_pkey PRIMARY KEY (id ASC),
    CONSTRAINT serverinstance_ukey UNIQUE (serverproductcodeid, zoneid, regionid, vpcid, subnetid, serverinstanceno),
	CONSTRAINT serverinstance_serverproductcodeid_fkey FOREIGN KEY (serverproductcodeid) REFERENCES product(id),
	CONSTRAINT serverinstance_zoneid_fkey FOREIGN KEY (zoneid) REFERENCES zone(id),
	CONSTRAINT serverinstance_regionid_fkey FOREIGN KEY (regionid) REFERENCES region(id),
	CONSTRAINT serverinstance_vpcid_fkey FOREIGN KEY (vpcid) REFERENCES vpc(id),
	CONSTRAINT serverinstance_subnetid_fkey FOREIGN KEY (subnetid) REFERENCES subnet(id)
);

CREATE TABLE IF NOT EXISTS activitylog (
	id INTEGER NOT NULL DEFAULT NEXTVAL('activitylog_seq'),
	zoneid INT8 NOT NULL,
	serverinstanceid INT8 NOT NULL,
	autoscalinggroupid INT8 NOT NULL,
	activityno VARCHAR(255) NOT NULL,
	-- serverinstanceno VARCHAR(255) NULL,
	zonecode VARCHAR(255) NULL,
	actionname VARCHAR(255) NOT NULL,
	actionstatus VARCHAR(255) NOT NULL,
	actioncause VARCHAR(255) NULL,
	actiondescription VARCHAR(255) NOT NULL,
	starttime TIMESTAMP NOT NULL,
	endtime TIMESTAMP NULL,
	CONSTRAINT activitylog_pkey PRIMARY KEY (id ASC),
    CONSTRAINT activitylog_ukey UNIQUE (zoneid, serverinstanceid, autoscalinggroupid, activityno),
	CONSTRAINT activitylog_zoneid_fkey FOREIGN KEY (zoneid) REFERENCES zone(id),
	CONSTRAINT activitylog_serverinstanceid_fkey FOREIGN KEY (serverinstanceid) REFERENCES serverinstance(id),
	CONSTRAINT activitylog_autoscalinggroupid_fkey FOREIGN KEY (autoscalinggroupid) REFERENCES autoscalinggroup(id)
  );
  
CREATE TABLE targetgroup (
	id INTEGER NOT NULL DEFAULT NEXTVAL ('targetgroup_seq'),
    targetGroupNo VARCHAR(255) NOT NULL,
    targetGroupName VARCHAR(255) NOT NULL,
    targetType VARCHAR(255) NOT NULL,
    vpcid INT8 NOT NULL,
    targetGroupProtocolType VARCHAR(255) NOT NULL,
    targetGroupPort VARCHAR(255) NOT NULL,
    targetGroupDescription VARCHAR(255) NULL,
    useStickySession BOOL NOT NULL,
    useProxyProtocol BOOL NOT NULL,
    algorithmType VARCHAR(255) NOT NULL,
    createDate TIMESTAMP NOT NULL,
    regionid INT8 NOT NULL,
    loadBalancerInstanceNo VARCHAR(255) NULL,
    healthCheckProtocolType VARCHAR(255) NOT NULL,
    healthCheckPort VARCHAR(255) NOT NULL,
    healthCheckUrlPath VARCHAR(255) NULL,
    healthCheckHttpMethodType VARCHAR(255) NULL,
    healthCheckCycle VARCHAR(255) NOT NULL,
    healthCheckUpThreshold VARCHAR(255) NOT NULL,
    healthCheckDownThreshold VARCHAR(255) NOT NULL,
    targetNoList VARCHAR(255) NULL,
	CONSTRAINT targetgroup_pkey PRIMARY KEY (id ASC),
	CONSTRAINT targetgroup_ukey UNIQUE (targetGroupNo, vpcid, regionid),
	CONSTRAINT targetgroup_regionid_fkey FOREIGN KEY (regionid) REFERENCES region(id),
	CONSTRAINT targetgroup_vpcid_fkey FOREIGN KEY (vpcid) REFERENCES vpc(id)
);

CREATE TABLE recoveryplan (
	id INTEGER NOT NULL DEFAULT NEXTVAL ('recoveryplan_seq'),
	requestid VARCHAR(255) NOT NULL,
	resourcetype VARCHAR(255) NOT NULL,
	sourcekey VARCHAR(255) NOT NULL,
	timestamp TIMESTAMP NOT NULL,
	command VARCHAR(255) NOT NULL,
	detail JSONB,
	completeflag BOOLEAN NOT NULL,
	CONSTRAINT recoveryplan_pkey PRIMARY KEY (id ASC)
);

CREATE TABLE recoveryresults (
	id INTEGER NOT NULL DEFAULT NEXTVAL ('recoveryresults_seq'),
	requestid VARCHAR(255) NOT NULL,
	resourcetype VARCHAR(255) NOT NULL,
	targetkey VARCHAR(255) NOT NULL,
	sourcekey VARCHAR(255) NOT NULL,
	timestamp TIMESTAMP NOT NULL,
	status VARCHAR(255) NOT NULL,
	detail JSONB,
	CONSTRAINT recoveryresults_pkey PRIMARY KEY (id ASC)
	--- CONSTRAINT recoveryresults_sourcekey_fkey FOREIGN KEY (sourcekey) REFERENCES recoveryplan(sourcekey)
);