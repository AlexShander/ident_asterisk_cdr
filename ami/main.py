from pyami_asterisk import AMIClient
import redis
import json
import time
from config import Config

class PassAMIChannelToRedis():
    def __init__(self, ami_host='127.0.0.1', ami_port=5038, ami_username='admin', 
                 ami_secret='password', redis_host='127.0.0.1', 
                 redis_port=6379, redis_db=0):
        self._ami = AMIClient(host=ami_host, port=ami_port, 
                              username=ami_username, secret=ami_secret)
        self.channels = list()
        self._redis = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

    def start_in_call(self, events):
        print('start_in_call', events)
        id_call = events.get('identifier', None)
        call_info = {
                     'direction' : 'in',
                     'phone_from' : events.get('FROM', None), 
                     'phone_to' : events.get('TO', None) ,
                     'start_call_time' : events.get('datetime', int(time.time())), 
                     'start_talk_time' : None, 
                     'line_description' : None,
                     'record_url' : None,
                    }
        if id_call is not None and events.get('FROM', None) is not None \
                               and events.get('TO', None) is not None:
            self._redis.setex(f"call:{id_call}", 3600, value=json.dumps(call_info)) 

    def call_to_operator(self, events):
        print('call_to_operator', events)
        id_call = events.get('identifier', None)
        operator = events.get('operator', None)
        if id_call is not None and operator is not None:
            call_info_str = self._redis.get(f"call:{id_call}")
            if call_info_str is not None:
                call_info = json.loads(call_info_str)
                call_info['line_description'] = events.get('operator', None)
                ttl = int(self._redis.pttl(f"call:{id_call}") / 1000)
                self._redis.setex(f"call:{id_call}", ttl, value=json.dumps(call_info))

    def answer_operator(self, events):
        print('answer_operator', events)
        id_call = events.get('identifier', None)
        operator = events.get('operator', None)
        if id_call is not None and operator is not None:
            call_info_str = self._redis.get(f"call:{id_call}") 
            if call_info_str is not None:
                call_info = json.loads(call_info_str)
                call_info['line_description'] = operator
                call_info['start_talk_time'] = events.get('datetime', int(time.time()))
                ttl = int(self._redis.pttl(f"call:{id_call}") / 1000)
                self._redis.setex(f"call:{id_call}", ttl, value=json.dumps(call_info))

    def endcall_to_operator(self, events):
        print('endcall_to_operator', events)
        id_call = events.get('identifier', None)
        operator = events.get('operator', None)
        if id_call is not None and operator is not None:
            call_info_str = self._redis.get(f"call:{id_call}")
            if call_info_str is not None:
                call_info = json.loads(call_info_str)
                if call_info.get('line_description') == operator:
                    call_infop['line_description'] = None
                    ttl = int(self._redis.pttl(f"call:{id_call}") / 1000)
                    self._redis.setex(f"call:{id_call}", ttl, value=json.dumps(call_info))

    def end_in_call(self, events):
        print('end_in_call', events)
        id_call = events.get('identifier', None)
        if id_call is not None:
            self._redis.delete(f"call:{id_call}")

    def start_out_call(self, events):
        print('start_out_call', events)
        id_call = events.get('identifier', None)
        call_info = {
                     'direction' : 'out',
                     'phone_from' : events.get('FROM', None),
                     'phone_to' : events.get('TO', None),
                     'start_call_time' : events.get('datetime', int(time.time())),
                     'start_talk_time' : None,
                     'line_description' : events.get('operator', None),
                     'record_url' : None,
                    }
        if id_call is not None and events.get('FROM', None) is not None \
                               and events.get('TO', None) is not None:
            self._redis.setex(f"call:{id_call}", 3600, value=json.dumps(call_info))


    def answer_out_call(self, events):
        print('answer_out_call', events)
        id_call = events.get('identifier', None)
        if id_call is not None: 
            call_info_str = self._redis.get(f"call:{id_call}")
            if call_info_str is not None:
                call_info = json.loads(call_info_str)
                call_info['start_talk_time'] = events.get('datetime', int(time.time()))
                ttl = int(self._redis.pttl(f"call:{id_call}") / 1000)
                self._redis.setex(f"call:{id_call}", ttl, value=json.dumps(call_info))

    def end_out_call(self, events):
        print('end_out_call', events)
        id_call = events.get('identifier', None)
        if id_call is not None:
            self._redis.delete(f"call:{id_call}")

    def get_channels(self):
        self._ami.register_event(["start-in-call"], self.start_in_call)
        self._ami.register_event(["call-to-operator"], self.call_to_operator)
        self._ami.register_event(["endcall-to-operator"], self.endcall_to_operator)
        self._ami.register_event(["answer-operator"], self.answer_operator)
        self._ami.register_event(["end-in-call"], self.end_in_call)
        self._ami.register_event(["start-out-call"], self.start_out_call)
        self._ami.register_event(["answer-out-call"], self.answer_out_call)
        self._ami.register_event(["end-out-call"], self.end_out_call)
        self._ami.connect()


def main():
    config = Config()
    ami_channel = PassAMIChannelToRedis(ami_host=config.AMI_ADDRESS, 
                                        ami_port=int(config.AMI_PORT),
                                        ami_username=config.AMI_USER,
                                        ami_secret=config.AMI_PASSWORD,
                                        redis_host=config.REDIS_HOST,
                                        redis_port=int(config.REDIS_PORT),
                                        redis_db=int(config.REDIS_DB))
    ami_channel.get_channels()


if __name__ == '__main__':
    main()
