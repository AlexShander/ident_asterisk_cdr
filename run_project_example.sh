#!/bin/bash

set -x

AMI_USER=userevents AMI_PASSWORD=password AMI_ADDRESS=172.17.0.1 IS_FIRST_SYNC=0 IDENT_INTEGRATION_KEY=secretIdent MYSQL_USER=asterisk MYSQL_PASSWORD=password MYSQL_ADDRESS=172.17.0.1 DOMAIN="https://$(hostname)/calls/records/"  DIR_RECORD="/var/spool/asterisk/monitor/" docker-compose up -d --build
