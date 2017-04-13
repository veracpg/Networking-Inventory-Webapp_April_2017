CREATE TABLE
    host
    (
        id INTEGER DEFAULT nextval('hosts_id_seq'::regclass) NOT NULL,
        hostname CHARACTER VARYING(128) NOT NULL,
        host_alias CHARACTER VARYING(128),
        hostgroup CHARACTER VARYING(128),
        ipv4 INET NOT NULL,
        ipv6 INET,
        os CHARACTER VARYING(128),
        os_type CHARACTER VARYING(128),
        os_release CHARACTER VARYING(128),
        ssh_port CHARACTER VARYING(128) DEFAULT '22',
        ssh_user CHARACTER VARYING(128) DEFAULT 'root'::CHARACTER VARYING,
        CONSTRAINT hosts_pkey PRIMARY KEY (id),
        UNIQUE (ipv4),
        UNIQUE (ipv6),
        UNIQUE (hostname)
    );