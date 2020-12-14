#!/bin/bash
export FLASK_APP=ident_cdr
export IDENT_INTEGRATION_KEY=1234567
export MYSQL_USER=root
export MYSQL_PASSWORD=3nf82s
export AMI_USER=userevents
export AMI_PASSWORD=password
flask run
