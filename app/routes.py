# -*- coding: utf-8 -*-
from flask import abort
from flask import jsonify
from flask import request
from app import app
from cdr import Cdr
from cdr import DBCdr
from config import Config
from datetime import datetime
from dateutil import tz
from dateutil import parser
from cdr_redis import GetChannelsFromRedis
import cdr_test


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
    date_time_from = parser.isoparse(request.args.get('dateTimeFrom', None)).astimezone(tz.tzlocal())
    date_time_to = parser.isoparse(request.args.get('dateTimeTo', None)).astimezone(tz.tzlocal())
    limit = request.args.get('limit', 500)
    offset = request.args.get('offset', 0)
    db_cdr = DBCdr()
    return jsonify(db_cdr.get_cdrs(date_time_from, date_time_to, limit, offset))


@app.route("/GetOngoingCalls", methods=['GET'])
def get_get_ingoing_calls():
    authorized_key = request.headers.get('IDENT-Integration-Key')
#    if authorized_key != app.config['IDENT_INTEGRATION_KEY']:
#        abort(404, description="Resource not found")
    limit = request.args.get('limit', 500)
    offset = request.args.get('offset', 0)
    get_channels = GetChannelsFromRedis()
    return jsonify(test_json())
