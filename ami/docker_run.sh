#!/bin/bash

sudo docker run -e AMI_USER=userevents -e AMI_PASSWORD=password -e AMI_ADDRESS=172.17.0.1  -e REDIS_HOST=172.17.0.3 -d  -it ami_collector
