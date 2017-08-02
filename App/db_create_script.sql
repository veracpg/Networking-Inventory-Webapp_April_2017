
-- Drop Database if exists before starting test

DROP DATABASE IF EXISTS hosts;

--Create Database
CREATE DATABASE hosts;

--Connect to database
\c hosts

--Create sequence

CREATE SEQUENCE host_id_seq INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START WITH 1 NO
CYCLE;

--Create host table
CREATE TABLE
    host
    (
        id INTEGER DEFAULT nextval('host_id_seq'::regclass) NOT NULL,
        hostname CHARACTER VARYING(128) NOT NULL,
        host_alias CHARACTER VARYING(128),
        hostgroup CHARACTER VARYING(128),
        ipv4 INET NOT NULL,
        ipv6 INET DEFAULT '2001:DB8:2222:7744::/64',
        os CHARACTER VARYING(128),
        os_type CHARACTER VARYING(128),
        os_release CHARACTER VARYING(128),
        ssh_port CHARACTER VARYING(128) DEFAULT '22',
        ssh_user CHARACTER VARYING(128) DEFAULT 'root'::CHARACTER VARYING,
        active BOOLEAN DEFAULT true,
        CONSTRAINT host_pkey PRIMARY KEY (id),
        UNIQUE (ipv4),
        UNIQUE (ipv6),
        UNIQUE (hostname)
    );

-- Test host_id

INSERT INTO host (hostname, host_alias, hostgroup, ipv4, ipv6, os, os_type, os_release, ssh_port, ssh_user, active)
VALUES ('BF-C33NL', null, 'blazingfast', '85.151.2.83', null,
                    'linux', 'CentOS', '6.7', '22', 'root', false);
INSERT INTO host (hostname, host_alias, hostgroup, ipv4, ipv6, os, os_type, os_release, ssh_port, ssh_user, active)
VALUES ('BF-C37NL', null, 'blazingfast', '85.151.2.78', null,
                    'linux', 'CentOS', '6.7', '22', 'root', false);
INSERT INTO host (hostname, host_alias, hostgroup, ipv4, ipv6, os, os_type, os_release, ssh_port, ssh_user, active)
VALUES ('BF-C4NL', null, 'blazingfast', '85.151.2.30', null,
                   'linux', 'CentOS', '6.7', '22', 'root', false);
INSERT INTO host (hostname, host_alias, hostgroup, ipv4, ipv6, os, os_type, os_release, ssh_port, ssh_user, active)
VALUES ('BF-C5P', null, 'blazingfast', '85.151.2.173', null,
                  'linux', 'Ubuntu', '16.04', '22', 'root', true);
INSERT INTO host (hostname, host_alias, hostgroup, ipv4, ipv6, os, os_type, os_release, ssh_port, ssh_user, active)
VALUES ('BF-C1P', null, 'blazingfast', '85.151.2.84', null,
                  'linux', 'Ubuntu', '16.04', '22', 'root', true);
INSERT INTO host (hostname, host_alias, hostgroup, ipv4, ipv6, os, os_type, os_release, ssh_port, ssh_user, active)
VALUES ('BF-C3P', null, 'blazingfast', '85.151.2.95', null,
                  'linux', 'Ubuntu', '16.04', '22', 'root', true);
INSERT INTO host (hostname, host_alias, hostgroup, ipv4, ipv6, os, os_type, os_release, ssh_port, ssh_user, active)
VALUES ('BF-C4P', null, 'blazingfast', '85.151.2.171', null,
                  'linux', 'Ubuntu', '16.04', '22', 'root', true);
