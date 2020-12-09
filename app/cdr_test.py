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
