import redis
import ast


class GetChannelsFromRedis():
    def __init__(self, host='127.0.0.1', port=6379, db=0):
        self._redis = redis.Redis(host=host, port=port, db=db)

    def _eval_to_dict(self, any_string: str):
        try:
            ev = ast.literal_eval(any_string)
            return ev
        except ValueError:
            corrected = any_string.replace('null', 'None')
            ev = ast.literal_eval(corrected)
            return ev

    def get_list_calls(self):
        cdr_list = list()
        for scan in self._redis.scan_iter(match='call:*'):
            cdr_str = self._redis.get(scan).decode("utf-8")
            cdr = self._eval_to_dict(cdr_str)
            cdr_list.append(cdr)
        return cdr_list

    def close(self):
        self._redis.close()

