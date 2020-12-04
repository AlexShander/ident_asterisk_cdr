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


def test_json():
    cdr = Cdr(date_and_time="2017-01-25T12:30:54+03:00",
              direction="in",
              phone_from="+79116844567",
              phone_to="+78126497035",
              wait_in_seconds=30,
              talk_in_seconds=10,
              record_url="http://google.com"
             )
    cdr1 = Cdr(date_and_time="2017-01-25T12:30:54+03:00",
               direction="in",
               phone_from="+79116844567",
               phone_to="+78126497035",
               wait_in_seconds=30,
               talk_in_seconds=10,
               record_url="http://google.com"
              )
    cdrs = [cdr.__dict__, cdr1.__dict__]
    return cdrs


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
    if authorized_key != app.config['IDENT_INTEGRATION_KEY']:
        abort(404, description="Resource not found")
    limit = request.args.get('limit', 500)
    offset = request.args.get('offset', 0)
    return jsonify(test_json())
