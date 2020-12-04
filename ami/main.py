from pyami_asterisk import AMIClient
import redis
import sys
sys.path.append('../')
import cdr 

class PassAMIChannelToRedis():
    def __init__(self, ami_host='127.0.0.1', ami_port=5038, ami_username='admin', 
                 ami_secret='password', redis_host='127.0.0.1', 
                 redis_port=6379, db=0):
        self._ami = AMIClient(host=ami_host, port=ami_port, 
                              username=ami_username, secret=ami_secret)
        self.channels = list()
        self._redis = redis.Redis(host=redis_host, port=redis_port, db=db)

    def parce_redis_calls():
        pass

    def parse_channel(self, events):
        print('parse_channel', events)
        if events.get('Event', None) == 'CoreShowChannelsComplete':
            print(None)
 
    def start_in_call(self, events):
        print('start_in_call', events)
        pass

    def call_to_operator(self, events):
        print('call_to_operator', events)
        pass

    def answer_operator(self, events):
        print('answer_operator', events)
        pass

    def endcall_to_operator(self, events):
        print('endcall_to_operator', events)
        pass

    def end_in_call(self, events):
        print('end_in_call', events)
        pass

    def start_out_call(self, events):
        print('start_out_call', events)
        pass

    def answer_out_call(self, events):
        print('answer_out_call', events)
        pass

    def end_out_call(self, events):
        print('end_out_call', events)
        pass

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


def test_module():
    ami_channel = PassAMIChannelToRedis(ami_host='127.0.0.1', ami_port=5038, 
                                        ami_username='userevents', 
                                        ami_secret='password',
                                        redis_host='127.0.0.1',
                                        redis_port=6379)
    ami_channel.get_channels()


def main():
    test_module()


if __name__ == '__main__':
    main()
