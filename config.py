import os

class Config(object):
    IDENT_INTEGRATION_KEY = os.environ.get('IDENT_INTEGRATION_KEY')
    AMI_USER = os.environ.get('AMI_USER') or 'admin'
    AMI_PASSWORD = os.environ.get('AMI_PASSWORD') or 'password'
    AMI_ADDRESS = os.environ.get('AMI_ADDRESS') or '127.0.0.1'
    AMI_PORT = os.environ.get('AMI_PORT') or '5038'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_ADDRESS = os.environ.get('MYSQL_ADDRESS') or '127.0.0.1'
    MYSQL_PORT = os.environ.get('MYSQL_PORT') or '3306'
    REDIS_HOST = os.environ.get('REDIST_HOST') or '127.0.0.1'
    REDIS_PORT = os.environ.get('REDIS_PORT') or '6379'
    REDIS_DB = os.environ.get('REDIS_DB') or '0'


