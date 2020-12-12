import os

class Config(object):
    AMI_USER = os.environ.get('AMI_USER') or 'userevents'
    AMI_PASSWORD = os.environ.get('AMI_PASSWORD') or 'password'
    AMI_ADDRESS = os.environ.get('AMI_ADDRESS') or '127.0.0.1'
    AMI_PORT = os.environ.get('AMI_PORT') or '5038'
    REDIS_HOST = os.environ.get('REDIS_HOST') or '127.0.0.1'
    REDIS_PORT = os.environ.get('REDIS_PORT') or '6379'
    REDIS_DB = os.environ.get('REDIS_DB') or '0'


