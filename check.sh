#!/bin/bash

curl -vvvvvvvvv -H "Accept: application/json" -H "IDENT-Integration-Key: 1234567" "http://127.0.0.1:5000/GetFinishedCalls?dateTimeFrom=2020-11-24T08:00:00%2B06:00&dateTimeTo=2020-11-24T10:00:00%2B06:00&limit=500&offset=0"

curl -vvvvvvvvv -H "Accept: application/json" -H "IDENT-Integration-Key: 1234567" "http://127.0.0.1:5000/GetOngoingCalls?dateTimeFrom=2020-11-24T08:00:00%2B06:00&dateTimeTo=2020-11-24T10:00:00%2B06:00&limit=500&offset=0"
