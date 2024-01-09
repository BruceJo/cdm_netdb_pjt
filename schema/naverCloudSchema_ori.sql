-- accesscontrolgroup definition

-- Drop table

-- DROP TABLE accesscontrolgroup;

CREATE TABLE accesscontrolgroup (
	id INT8 NOT NULL DEFAULT unique_rowid(),
	accesscontrolgroupno VARCHAR(255) NOT NULL,
	accesscontrolgroupname VARCHAR(255) NOT NULL,
	isdefault BOOL NOT NULL,
	vpcno VARCHAR(255) NOT NULL,
	accesscontrolgroupstatus VARCHAR(255) NOT NULL,
	accesscontrolgroupdescription VARCHAR(255) NULL,
	CONSTRAINT accesscontrolgroup_pkey PRIMARY KEY (id ASC)
);


-- adjustmenttype definition

-- Drop table

-- DROP TABLE adjustmenttype;

CREATE TABLE adjustmenttype (
	id INT8 NOT NULL DEFAULT unique_rowid(),
	code VARCHAR(255) NOT NULL,
	codename VARCHAR(255) NOT NULL,
	CONSTRAINT adjustmenttype_pkey PRIMARY KEY (id ASC)
);


-- inautoscalinggroupserverinstance definition

-- Drop table

-- DROP TABLE inautoscalinggroupserverinstance;

CREATE TABLE inautoscalinggroupserverinstance (
	id INT8 NOT NULL DEFAULT unique_rowid(),
	serverinstanceno VARCHAR(255) NULL,
	healthstatus VARCHAR(255) NULL,
	lifecyclestate VARCHAR(255) NULL,
	CONSTRAINT inautoscalinggroupserverinstance_pkey PRIMARY KEY (id ASC)
);


-- initscript definition

-- Drop table

-- DROP TABLE initscript;

CREATE TABLE initscript (
	id INT8 NOT NULL DEFAULT unique_rowid(),
	initscriptno VARCHAR(255) NOT NULL,
	initscriptname VARCHAR(255) NOT NULL,
	createdate TIMESTAMP NOT NULL,
	initscriptdescription VARCHAR(255) NULL,
	initscriptcontent STRING NOT NULL,
	ostype VARCHAR(255) NOT NULL,
	CONSTRAINT initscript_pkey PRIMARY KEY (id ASC)
);


-- loadbalancerruleaction definition

-- Drop table

-- DROP TABLE loadbalancerruleaction;

CREATE TABLE loadbalancerruleaction (
	id INT8 NOT NULL DEFAULT unique_rowid(),
	ruleactiontype VARCHAR(255) NOT NULL,
	targetgroupaction VARCHAR(255) NULL,
	redirectionaction VARCHAR(255) NULL,
	CONSTRAINT loadbalancerruleaction_pkey PRIMARY KEY (id ASC)
);


-- loadbalancerrulecondition definition

-- Drop table

-- DROP TABLE loadbalancerrulecondition;

CREATE TABLE loadbalancerrulecondition (
	id INT8 NOT NULL DEFAULT unique_rowid(),
	ruleconditiontype VARCHAR(255) NOT NULL,
	hostheadercondition VARCHAR(255) NULL,
	pathpatterncondition VARCHAR(255) NULL,
	CONSTRAINT loadbalancerrulecondition_pkey PRIMARY KEY (id ASC)
);


-- loginkey definition

-- Drop table

-- DROP TABLE loginkey;

CREATE TABLE loginkey (
	id INT8 NOT NULL DEFAULT unique_rowid(),
	fingerprint VARCHAR(255) NOT NULL,
	keyname VARCHAR(255) NOT NULL,
	createdate TIMESTAMP NOT NULL,
	CONSTRAINT loginkey_pkey PRIMARY KEY (id ASC)
);


-- memberserverimageinstance definition

-- Drop table

-- DROP TABLE memberserverimageinstance;

CREATE TABLE memberserverimageinstance (
	id INT8 NOT NULL DEFAULT unique_rowid(),
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
	sharedloginidlist STRING NOT NULL,
	CONSTRAINT memberserverimageinstance_pkey PRIMARY KEY (id ASC)
);


-- placementgroup definition

-- Drop table

-- DROP TABLE placementgroup;

CREATE TABLE placementgroup (
	id INT8 NOT NULL DEFAULT unique_rowid(),
	placementgroupno VARCHAR(255) NOT NULL,
	placementgroupname VARCHAR(255) NOT NULL,
	placementgrouptype VARCHAR(255) NOT NULL,
	CONSTRAINT placementgroup_pkey PRIMARY KEY (id ASC)
);


-- product definition

-- Drop table

-- DROP TABLE product;

CREATE TABLE product (
	id INT8 NOT NULL DEFAULT unique_rowid(),
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
	CONSTRAINT product_pkey PRIMARY KEY (id ASC)
);


-- protocoltype definition

-- Drop table

-- DROP TABLE protocoltype;

CREATE TABLE protocoltype (
	id INT8 NOT NULL DEFAULT unique_rowid(),
	code VARCHAR(255) NOT NULL,
	codename VARCHAR(255) NOT NULL,
	codenumber INT8 NOT NULL,
	CONSTRAINT protocoltype_pkey PRIMARY KEY (id ASC)
);


-- publicipinstance definition

-- Drop table

-- DROP TABLE publicipinstance;

CREATE TABLE publicipinstance (
	id INT8 NOT NULL DEFAULT unique_rowid(),
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


-- "region" definition

-- Drop table

-- DROP TABLE "region";

CREATE TABLE region (
	id INT8 NOT NULL DEFAULT unique_rowid(),
	regioncode VARCHAR(255) NOT NULL,
	regionname VARCHAR(255) NOT NULL,
	CONSTRAINT region_pkey PRIMARY KEY (id ASC)
);


-- accesscontrolgrouprule definition

-- Drop table

-- DROP TABLE accesscontrolgrouprule;

CREATE TABLE accesscontrolgrouprule (
	id INT8 NOT NULL DEFAULT unique_rowid(),
	accesscontrolgroupid INT8 NOT NULL,
	protocoltypeid INT8 NOT NULL,
	ipblock VARCHAR(255) NULL,
	accesscontrolgroupsequence VARCHAR(255) NULL,
	portrange VARCHAR(255) NULL,
	accesscontrolgroupruletype VARCHAR(255) NOT NULL,
	accesscontrolgroupruledescription VARCHAR(255) NOT NULL,
	CONSTRAINT accesscontrolgrouprule_pkey PRIMARY KEY (id ASC),
	CONSTRAINT accesscontrolgrouprule_accesscontrolgroupid_fkey FOREIGN KEY (accesscontrolgroupid) REFERENCES accesscontrolgroup(id),
	CONSTRAINT accesscontrolgrouprule_protocoltypeid_fkey FOREIGN KEY (protocoltypeid) REFERENCES protocoltype(id)
);


-- launchconfiguration definition

-- Drop table

-- DROP TABLE launchconfiguration;

CREATE TABLE launchconfiguration (
	id INT8 NOT NULL DEFAULT unique_rowid(),
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
	CONSTRAINT launchconfiguration_pkey PRIMARY KEY (launchconfigurationno ASC),
	CONSTRAINT launchconfiguration_regionid_fkey FOREIGN KEY (regionid) REFERENCES region(id),
	CONSTRAINT launchconfiguration_serverproductid_fkey FOREIGN KEY (serverproductid) REFERENCES product(id),
	CONSTRAINT launchconfiguration_loginkeyid_fkey FOREIGN KEY (loginkeyid) REFERENCES loginkey(id)
);


-- vpc definition

-- Drop table

-- DROP TABLE vpc;

CREATE TABLE vpc (
	id INT8 NOT NULL DEFAULT unique_rowid(),
	regionid INT8 NOT NULL,
	vpcno VARCHAR(255) NOT NULL,
	vpcname VARCHAR(255) NOT NULL,
	ipv4cidrblock VARCHAR(255) NOT NULL,
	vpcstatus VARCHAR(255) NOT NULL,
	createdate TIMESTAMP NOT NULL,
	CONSTRAINT vpc_pkey PRIMARY KEY (id ASC),
	CONSTRAINT vpc_regionid_fkey FOREIGN KEY (regionid) REFERENCES region(id)
);


-- vpcpeeringinstance definition

-- Drop table

-- DROP TABLE vpcpeeringinstance;

CREATE TABLE vpcpeeringinstance (
	id INT8 NOT NULL DEFAULT unique_rowid(),
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
	CONSTRAINT vpcpeeringinstance_regionid_fkey FOREIGN KEY (regionid) REFERENCES region(id),
	CONSTRAINT vpcpeeringinstance_sourcevpcid_fkey FOREIGN KEY (sourcevpcid) REFERENCES vpc(id),
	CONSTRAINT vpcpeeringinstance_targetvpcid_fkey FOREIGN KEY (targetvpcid) REFERENCES vpc(id)
);


-- "zone" definition

-- Drop table

-- DROP TABLE "zone";

CREATE TABLE zone (
	id INT8 NOT NULL DEFAULT unique_rowid(),
	regionid INT8 NOT NULL,
	zonename VARCHAR(255) NOT NULL,
	zonecode VARCHAR(255) NOT NULL,
	zonedescription VARCHAR(255) NOT NULL,
	CONSTRAINT zone_pkey PRIMARY KEY (id ASC),
	CONSTRAINT zone_regionid_fkey FOREIGN KEY (regionid) REFERENCES region(id)
);


-- blockstorageinstance definition

-- Drop table

-- DROP TABLE blockstorageinstance;

CREATE TABLE blockstorageinstance (
	id INT8 NOT NULL DEFAULT unique_rowid(),
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
	CONSTRAINT blockstorageinstance_zoneid_fkey FOREIGN KEY (zoneid) REFERENCES zone(id),
	CONSTRAINT blockstorageinstance_regionid_fkey FOREIGN KEY (regionid) REFERENCES region(id)
);


-- blockstoragesnapshotinstance definition

-- Drop table

-- DROP TABLE blockstoragesnapshotinstance;

CREATE TABLE blockstoragesnapshotinstance (
	id INT8 NOT NULL DEFAULT unique_rowid(),
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
	CONSTRAINT blockstoragesnapshotinstance_blockstoragenstanceid_fkey FOREIGN KEY (blockstorageinstanceid) REFERENCES blockstorageinstance(id)
);


-- loadbalancerinstance definition

-- Drop table

-- DROP TABLE loadbalancerinstance;

CREATE TABLE loadbalancerinstance (
	id INT8 NOT NULL DEFAULT unique_rowid(),
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
	loadbalanceriplist STRING NULL,
	loadbalancertype VARCHAR(255) NOT NULL,
	loadbalancernetworktype VARCHAR(255) NOT NULL,
	throughputtype VARCHAR(255) NOT NULL,
	idletimeout INT8 NULL,
	subnetnolist VARCHAR(255) NOT NULL,
	loadbalancersubnetlist VARCHAR(255) NOT NULL,
	loadbalancerlistenernolist VARCHAR(255) NULL,
	CONSTRAINT loadbalancerinstance_pkey PRIMARY KEY (id ASC),
	CONSTRAINT loadbalancerinstance_vpcid_fkey FOREIGN KEY (vpcid) REFERENCES vpc(id),
	CONSTRAINT loadbalancerinstance_regionid_fkey FOREIGN KEY (regionid) REFERENCES region(id)
);


-- loadbalancerlistener definition

-- Drop table

-- DROP TABLE loadbalancerlistener;

CREATE TABLE loadbalancerlistener (
	id INT8 NOT NULL DEFAULT unique_rowid(),
	loadbalancerinstanceid INT8 NOT NULL,
	loadbalancerlistenerno VARCHAR(255) NOT NULL,
	protocoltype VARCHAR(50) NOT NULL,
	port INT8 NOT NULL,
	usehttp2 BOOL NOT NULL,
	sslcertificateno VARCHAR(255) NULL,
	tlsminversiontype VARCHAR(50) NULL,
	loadbalancerrulenolist VARCHAR(255) NOT NULL,
	ciphersuitelist VARCHAR(255) NOT NULL,
	CONSTRAINT loadbalancerlistener_pkey PRIMARY KEY (id ASC),
	CONSTRAINT loadbalancerlistener_loadbalancerinstanceid_fkey FOREIGN KEY (loadbalancerinstanceid) REFERENCES loadbalancerinstance(id)
);


-- loadbalancerrule definition

-- Drop table

-- DROP TABLE loadbalancerrule;

CREATE TABLE loadbalancerrule (
	id INT8 NOT NULL DEFAULT unique_rowid(),
	loadbalancerlistenerid INT8 NOT NULL,
	loadbalancerruleno VARCHAR(255) NOT NULL,
	priority INT8 NOT NULL,
	loadbalancerruleconditionlist VARCHAR(255) NOT NULL,
	loadbalancerruleactionlist VARCHAR(255) NOT NULL,
	CONSTRAINT loadbalancerrule_pkey PRIMARY KEY (id ASC),
	CONSTRAINT loadbalancerrule_loadbalancerlistenerid_fkey FOREIGN KEY (loadbalancerlistenerid) REFERENCES loadbalancerlistener(id)
);


-- memberserverimage definition

-- Drop table

-- DROP TABLE memberserverimage;

CREATE TABLE memberserverimage (
	id INT8 NOT NULL DEFAULT unique_rowid(),
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
	CONSTRAINT memberserverimage_zoneid_fkey FOREIGN KEY (zoneid) REFERENCES zone(id)
);


-- networkacl definition

-- Drop table

-- DROP TABLE networkacl;

CREATE TABLE networkacl (
	id INT8 NOT NULL DEFAULT unique_rowid(),
	vpcid INT8 NOT NULL,
	networkaclno VARCHAR(255) NOT NULL,
	networkaclname VARCHAR(255) NOT NULL,
	networkaclstatus VARCHAR(255) NOT NULL,
	networkacldescription VARCHAR(255) NULL,
	createdate TIMESTAMP NOT NULL,
	isdefault BOOL NOT NULL,
	CONSTRAINT networkacl_pkey PRIMARY KEY (id ASC),
	CONSTRAINT networkacl_vpcid_fkey FOREIGN KEY (vpcid) REFERENCES vpc(id)
);


-- networkacldenyallowgroup definition

-- Drop table

-- DROP TABLE networkacldenyallowgroup;

CREATE TABLE networkacldenyallowgroup (
	id INT8 NOT NULL DEFAULT unique_rowid(),
	vpcid INT8 NOT NULL,
	networkacldenyallowgroupno VARCHAR(255) NOT NULL,
	networkacldenyallowgroupname VARCHAR(255) NOT NULL,
	networkacldenyallowgroupstatus VARCHAR(255) NOT NULL,
	iplist STRING NULL,
	networkacldenyallowgroupdescription VARCHAR(255) NULL,
	createdate TIMESTAMP NOT NULL,
	isapplied BOOL NOT NULL,
	CONSTRAINT networkacldenyallowgroup_pkey PRIMARY KEY (id ASC),
	CONSTRAINT networkacldenyallowgroup_vpcid_fkey FOREIGN KEY (vpcid) REFERENCES vpc(id)
);


-- networkaclrule definition

-- Drop table

-- DROP TABLE networkaclrule;

CREATE TABLE networkaclrule (
	id INT8 NOT NULL DEFAULT unique_rowid(),
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
	CONSTRAINT networkaclrule_networkaclid_fkey FOREIGN KEY (networkaclid) REFERENCES networkacl(id),
	CONSTRAINT networkaclrule_protocolid_fkey FOREIGN KEY (protocolid) REFERENCES protocoltype(id)
);


-- routetable definition

-- Drop table

-- DROP TABLE routetable;

CREATE TABLE routetable (
	id INT8 NOT NULL DEFAULT unique_rowid(),
	regionid INT8 NOT NULL,
	vpcid INT8 NOT NULL,
	routetableno VARCHAR(255) NOT NULL,
	routetablename VARCHAR(255) NOT NULL,
	supportedsubnettype VARCHAR(255) NOT NULL,
	isdefault BOOL NOT NULL,
	routetablestatus VARCHAR(255) NOT NULL,
	routetabledescription VARCHAR(255) NULL,
	CONSTRAINT routetable_pkey PRIMARY KEY (id ASC),
	CONSTRAINT routetable_regionid_fkey FOREIGN KEY (regionid) REFERENCES region(id),
	CONSTRAINT routetable_vpcid_fkey FOREIGN KEY (vpcid) REFERENCES vpc(id)
);


-- subnet definition

-- Drop table

-- DROP TABLE subnet;

CREATE TABLE subnet (
	id INT8 NOT NULL DEFAULT unique_rowid(),
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
	CONSTRAINT subnet_vpcid_fkey FOREIGN KEY (vpcid) REFERENCES vpc(id),
	CONSTRAINT subnet_zoneid_fkey FOREIGN KEY (zoneid) REFERENCES zone(id),
	CONSTRAINT subnet_networkaclid_fkey FOREIGN KEY (networkaclid) REFERENCES networkacl(id)
);


-- autoscalinggroup definition

-- Drop table

-- DROP TABLE autoscalinggroup;

CREATE TABLE autoscalinggroup (
	id INT8 NOT NULL DEFAULT unique_rowid(),
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
	inautoscalinggroupserverinstancelist JSONB NULL,
	targetgroupnolist JSONB NULL,
	accesscontrolgroupnolist JSONB NOT NULL,
	suspendedprocesslist JSONB NULL,
	CONSTRAINT autoscalinggroup_pkey PRIMARY KEY (id ASC),
	CONSTRAINT autoscalinggroup_vpcid_fkey FOREIGN KEY (vpcid) REFERENCES vpc(id),
	CONSTRAINT autoscalinggroup_subnetid_fkey FOREIGN KEY (subnetid) REFERENCES subnet(id)
);


-- loadbalancersubnet definition

-- Drop table

-- DROP TABLE loadbalancersubnet;

CREATE TABLE loadbalancersubnet (
	id INT8 NOT NULL DEFAULT unique_rowid(),
	zoneid INT8 NOT NULL,
	subnetid INT8 NOT NULL,
	publicipinstanceid INT8 NULL,
	CONSTRAINT loadbalancersubnet_pkey PRIMARY KEY (id ASC),
	CONSTRAINT loadbalancersubnet_zoneid_fkey FOREIGN KEY (zoneid) REFERENCES zone(id),
	CONSTRAINT loadbalancersubnet_subnetid_fkey FOREIGN KEY (subnetid) REFERENCES subnet(id),
	CONSTRAINT loadbalancersubnet_publicipinstanceid_fkey FOREIGN KEY (publicipinstanceid) REFERENCES publicipinstance(id)
);


-- natgatewayinstance definition

-- Drop table

-- DROP TABLE natgatewayinstance;

CREATE TABLE natgatewayinstance (
	id INT8 NOT NULL DEFAULT unique_rowid(),
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
	CONSTRAINT natgatewayinstance_vpcid_fkey FOREIGN KEY (vpcid) REFERENCES vpc(id),
	CONSTRAINT natgatewayinstance_subnetid_fkey FOREIGN KEY (subnetid) REFERENCES subnet(id)
);


-- networkinterface definition

-- Drop table

-- DROP TABLE networkinterface;

CREATE TABLE networkinterface (
	id INT8 NOT NULL DEFAULT unique_rowid(),
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
	accesscontrolgroupnolist VARCHAR(255) NULL,
	networkinterfacedescription VARCHAR(255) NULL,
	secondaryiplist VARCHAR(255) NULL,
	CONSTRAINT networkinterface_pkey PRIMARY KEY (id ASC),
	CONSTRAINT networkinterface_subnetid_fkey FOREIGN KEY (subnetid) REFERENCES subnet(id)
);


-- route definition

-- Drop table

-- DROP TABLE route;

CREATE TABLE route (
	id INT8 NOT NULL DEFAULT unique_rowid(),
	routetableid INT8 NOT NULL,
	destinationcidrblock VARCHAR(255) NOT NULL,
	targetname VARCHAR(255) NOT NULL,
	targettype VARCHAR(255) NOT NULL,
	targetno VARCHAR(255) NOT NULL,
	isdefault BOOL NOT NULL,
	CONSTRAINT route_pkey PRIMARY KEY (id ASC),
	CONSTRAINT route_routetableid_fkey FOREIGN KEY (routetableid) REFERENCES routetable(id)
);


-- scalingpolicy definition

-- Drop table

-- DROP TABLE scalingpolicy;

CREATE TABLE scalingpolicy (
	id INT8 NOT NULL DEFAULT unique_rowid(),
	autoscalinggroupid INT8 NOT NULL,
	policyno VARCHAR(255) NOT NULL,
	policyname VARCHAR(255) NOT NULL,
	adjustmenttype VARCHAR(255) NOT NULL,
	scalingadjustment INT8 NOT NULL,
	minadjustmentstep INT8 NULL,
	cooldown INT8 NULL,
	CONSTRAINT scalingpolicy_pkey PRIMARY KEY (id ASC),
	CONSTRAINT scalingpolicy_autoscalinggroupid_fkey FOREIGN KEY (autoscalinggroupid) REFERENCES autoscalinggroup(id)
);


-- scheduledupdategroupaction definition

-- Drop table

-- DROP TABLE scheduledupdategroupaction;

CREATE TABLE scheduledupdategroupaction (
	id INT8 NOT NULL DEFAULT unique_rowid(),
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
	CONSTRAINT scheduledupdategroupaction_autoscalinggroupid_fkey FOREIGN KEY (autoscalinggroupid) REFERENCES autoscalinggroup(id)
);


-- serverinstance definition

-- Drop table

-- DROP TABLE serverinstance;

CREATE TABLE serverinstance (
	id INT8 NOT NULL DEFAULT unique_rowid(),
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
	networkinterfacenolist VARCHAR(255) NOT NULL,
	initscriptno VARCHAR(255) NULL,
	serverinstancetype VARCHAR(255) NOT NULL,
	baseblockstoragedisktype VARCHAR(255) NOT NULL,
	baseblockstoragediskdetailtype VARCHAR(255) NOT NULL,
	placementgroupno VARCHAR(255) NULL,
	placementgroupname VARCHAR(255) NULL,
	memberserverimageinstanceno VARCHAR(255) NULL,
	blockdevicepartitionlist VARCHAR(255) NULL,
	CONSTRAINT serverinstance_pkey PRIMARY KEY (id ASC),
	CONSTRAINT serverinstance_serverproductcodeid_fkey FOREIGN KEY (serverproductcodeid) REFERENCES product(id),
	CONSTRAINT serverinstance_zoneid_fkey FOREIGN KEY (zoneid) REFERENCES zone(id),
	CONSTRAINT serverinstance_regionid_fkey FOREIGN KEY (regionid) REFERENCES region(id),
	CONSTRAINT serverinstance_vpcid_fkey FOREIGN KEY (vpcid) REFERENCES vpc(id),
	CONSTRAINT serverinstance_subnetid_fkey FOREIGN KEY (subnetid) REFERENCES subnet(id)
);


-- activitylog definition

-- Drop table

-- DROP TABLE activitylog;

CREATE TABLE activitylog (
	id INT8 NOT NULL DEFAULT unique_rowid(),
	activityno VARCHAR(255) NOT NULL,
	autoscalinggroupid INT8 NOT NULL,
	serverinstanceno VARCHAR(255) NULL,
	zonecode VARCHAR(255) NULL,
	actionname VARCHAR(255) NOT NULL,
	actionstatus VARCHAR(255) NOT NULL,
	actioncause VARCHAR(255) NULL,
	actiondescription VARCHAR(255) NOT NULL,
	starttime TIMESTAMP NOT NULL,
	endtime TIMESTAMP NULL,
	CONSTRAINT activitylog_pkey PRIMARY KEY (id ASC),
	CONSTRAINT activitylog_autoscalinggroupid_fkey FOREIGN KEY (autoscalinggroupid) REFERENCES autoscalinggroup(id)
);