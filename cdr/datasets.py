from dateutil import tz 

class Cdr(object):
    """ The Cdr class contains record of one cdr.
        For example: 
        "DateAndTime": "2017-01-25T12:30:54+03:00",
        "Direction": "in",
        "PhoneFrom": "+79116844567",
        "PhoneTo": "+78126497035",
        "WaitInSeconds": 30,
        "TalkInSeconds": null,
        "RecordUrl": null.
    """
    def __init__(self, date_and_time, direction, phone_from, phone_to,
                 wait_in_seconds, talk_in_seconds, record_url, line_description):
        self._date_and_time = dict(descr='DateAndTime', data=date_and_time)
        self._direction =  dict(descr='Direction', data=direction)
        if phone_from == '':
            self._phone_from = dict(descr='PhoneFrom', data=None)
        else:
            self._phone_from = dict(descr='PhoneFrom', data=phone_from)
        if phone_to == '':
            self._phone_to = dict(descr='PhoneTo', data=None)
        else:
            self._phone_to = dict(descr='PhoneTo', data=phone_to)
        if wait_in_seconds < 1:
            self._wait_in_seconds = dict(descr='WaitInSeconds', data=None)
        else:
            self._wait_in_seconds = dict(descr='WaitInSeconds', data=wait_in_seconds)
        if talk_in_seconds < 1: 
            self._talk_in_seconds = dict(descr='TalkInSeconds', data=None)
        else:
            self._talk_in_seconds = dict(descr='TalkInSeconds', data=talk_in_seconds)
        if record_url == '':
            self._record_url == dict(descr='RecordUrl', data=None)
        else:
            self._record_url = dict(descr='RecordUrl', data=record_url)
        if line_description == '':
            self._line_description == dict(descr='RecordUrl', data=None)
        else:
            self._line_description = dict(descr='LineDescription', data=line_description)           
        self.__dict__= self.create_dict()

    def create_dict(self):
        """
            It does dict for serialize JSON.
        """
        cdr_dict = {self._date_and_time['descr']: self._date_and_time['data'].\
                        replace(tzinfo=tz.tzlocal()).\
                        isoformat(),
                    self._direction['descr']: self._direction['data'],
                    self._phone_from['descr']: self._phone_from['data'],
                    self._phone_to['descr']: self._phone_to['data'],
                    self._wait_in_seconds['descr']: self._wait_in_seconds['data'],
                    self._talk_in_seconds['descr']: self._talk_in_seconds['data'],
                    self._record_url['descr']: self._record_url['data']},
                    self._line_description['descr']: self._line_description['data']}
        return cdr_dict


