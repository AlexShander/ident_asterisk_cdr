FROM python:3.7-alpine
LABEL maintaner="alexmasc05@gmail.com"

COPY . /var/app
WORKDIR /var/app
RUN /usr/local/bin/python -m pip install --upgrade pip && pip3 install -r requirements.txt

ENTRYPOINT ["/bin/sh", "runit.sh"]
