
#UDACITY - ITEM CATALOGUE PROJECT

##Project Description:

Develop an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.



##Tech:

Python / PostgreSQL / SQLalchemy / Flask Framework / HTML / CSS / JavaScript / AJAX / Oauth2

##Files:

- ##### db_connector.py

        Contains the implementation for the Network Inventory using Python & SQLalchemy API
        
- ##### db_create_script.sql

        Contains all the SQL code to create automatically 
        the Database, Tables and Views

        
- ##### __init__.py

        Contais the backend code to manage the Web App 

##Requirements:

Vagrant build for the Udacity tournament project, link below:

https://www.vagrantup.com/downloads.html

https://www.virtualbox.org/wiki/Downloads

https://d17h27t6h515a5.cloudfront.net/topher/2016/December/58488015_fsnd-virtual-machine/fsnd-virtual-machine.zip 

##How to test it:

- Install Vagrant with the configurations on Vagrant File

- Create the Demo Data Base with the following command:

    > psql -f db_create_script.sql

- Run the Web App with the following command:

    > python __init__.py

- Test the App with the following hosts:

    > INSERT INTO host (hostname, host_alias, hostgroup, ipv4, ipv6, os, os_type, os_release, ssh_port, ssh_user, active)
      VALUES ('BF-C33NL', null, 'blazingfast', '85.151.2.83', null,'linux', 'CentOS', '6.7', '22', 'root', True);

    > INSERT INTO host (hostname, host_alias, hostgroup, ipv4, ipv6, os, os_type, os_release, ssh_port, ssh_user, active)
      VALUES ('BF-C37NL', null, 'blazingfast', '85.151.2.78', null,'linux', 'CentOS', '6.7', '22', 'root', false);

    > INSERT INTO host (hostname, host_alias, hostgroup, ipv4, ipv6, os, os_type, os_release, ssh_port, ssh_user, active)
    VALUES ('BF-C4NL', null, 'blazingfast', '85.151.2.30', null, 'linux', 'CentOS', '6.7', '22', 'root', false);











