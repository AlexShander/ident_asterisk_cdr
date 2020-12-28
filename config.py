import os

class Config(object):
    IDENT_INTEGRATION_KEY = os.environ.get('IDENT_INTEGRATION_KEY')
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_ADDRESS = os.environ.get('MYSQL_ADDRESS') or '127.0.0.1'
    MYSQL_PORT = os.environ.get('MYSQL_PORT') or '3306'
    REDIS_HOST = os.environ.get('REDIS_HOST') or '127.0.0.1'
    REDIS_PORT = os.environ.get('REDIS_PORT') or '6379'
    REDIS_DB = os.environ.get('REDIS_DB') or '0'
    DOMAIN = os.environ.get('DOMAIN') or ''
    DIR_RECORD = os.environ.get('DIR_RECORD')  or '0'
    IS_FIRST_SYNC = os.environ.get('IS_FIRST_SYNC') or '1'

