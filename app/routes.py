# -*- coding: utf-8 -*-
from flask import abort
from flask import jsonify
from flask import request
from app import app
from cdr import Cdr
from cdr import DBCdr
from datetime import datetime
from datetime import timedelta
from dateutil import tz
from dateutil import parser
from .cdr_redis import GetChannelsFromRedis


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.route("/cheese")
def get_one_cheese():
    resource = None 
    if resource is None:
        abort(404, description="Resource not found")
    return jsonify(resource)


@app.route("/GetFinishedCalls", methods=['GET'])
def get_finised_calls():
    authorized_key = request.headers.get('IDENT-Integration-Key')
#    if authorized_key != app.config['IDENT_INTEGRATION_KEY']:
#        abort(404, description="Resource not found")
    date_time_from  = parser.isoparse(request.args.get('dateTimeFrom', None)).astimezone(tz.tzlocal())
    ninety_days_ago = (datetime.now() - timedelta(days=90)).astimezone(tz.tzlocal())
    is_first_sync = app.config.get("IS_FIRST_SYNC")
    if is_first_sync  == "0" and ninety_days_ago > date_time_from:
        date_time_from = datetime.now()  - timedelta(days=3)
    date_time_to = parser.isoparse(request.args.get('dateTimeTo', None)).astimezone(tz.tzlocal())
    limit = request.args.get('limit', 500)
    offset = request.args.get('offSet', 0)
    db_cdr = DBCdr(mysql_user=app.config.get("MYSQL_USER"),
                   mysql_password=app.config.get("MYSQL_PASSWORD"),
                   mysql_address=app.config.get("MYSQL_ADDRESS"),
                   mysql_port=app.config.get("MYSQL_PORT"),
                   domain=app.config.get("DOMAIN"),
                   dir_record=app.config.get("DIR_RECORD")
                  )
    response = jsonify(db_cdr.get_cdrs(date_time_from, date_time_to, limit, offset))
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response


@app.route("/GetOngoingCalls", methods=['GET'])
def get_get_ingoing_calls():
    authorized_key = request.headers.get('IDENT-Integration-Key')
#    if authorized_key != app.config['IDENT_INTEGRATION_KEY']:
#        abort(404, description="Resource not found")
    limit = request.args.get('limit', 500)
    offset = request.args.get('offSet', 0)
    get_channels = GetChannelsFromRedis(host=app.config.get("REDIS_HOST"),
                                        port=app.config.get("REDIS_PORT"),
                                        db=app.config.get("REDIS_DB")
                                       )
    list_cdr = list()
    for tmp_cdr in get_channels.get_list_calls():
        start_call_time = datetime.fromtimestamp(int(tmp_cdr.get('start_call_time')))
        start_talk_time = 0 if tmp_cdr.get('start_talk_time', None) is None else int(tmp_cdr.get('start_talk_time', 0))
        if start_talk_time == 0:
            wait_in_seconds = int(datetime.now().timestamp()) - int(tmp_cdr.get('start_call_time'))
            talk_in_seconds = 0
        else:
            wait_in_seconds = start_talk_time - int(tmp_cdr.get('start_call_time'))
            talk_in_seconds = int(datetime.now().timestamp()) - start_talk_time 
        list_cdr.append(Cdr(start_call_time,
                            tmp_cdr.get('direction'),
                            tmp_cdr.get('phone_from'),
                            tmp_cdr.get('phone_to'),
                            wait_in_seconds,
                            talk_in_seconds,
                            None,
                            tmp_cdr.get('line_description')
                            ).__dict__
                       )

    get_channels.close()
    response = jsonify(list_cdr)
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response

