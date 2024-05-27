DROP TABLE IF EXISTS recoveryplan;
DROP TABLE IF EXISTS recoveryresults;

DROP SEQUENCE IF EXISTS recoveryplan_seq;
DROP SEQUENCE IF EXISTS recoveryresults_seq;

CREATE SEQUENCE IF NOT EXISTS recoveryplan_seq;
CREATE SEQUENCE IF NOT EXISTS recoveryresults_seq;

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