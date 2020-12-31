FROM python:3.8-alpine

LABEL maintainer="Alexandr Shander <alexmasc05@gmail.com>"

RUN apk add --no-cache python3-dev build-base linux-headers pcre-dev
RUN /usr/local/bin/python -m pip install --upgrade pip && pip3 install uwsgi flask
WORKDIR /ident_asterisk_cdr
COPY requirements.txt /ident_asterisk_cdr/
RUN pip3 install -r requirements.txt
COPY ./README.md /ident_asterisk_cdr/
COPY ./config.py /ident_asterisk_cdr/
COPY ./ident_cdr.py /ident_asterisk_cdr/
COPY ./app/ /ident_asterisk_cdr/app/
COPY ./cdr/ /ident_asterisk_cdr/cdr/

ENTRYPOINT ["uwsgi", "--socket=0.0.0.0:9988", "--protocol=http", "-w", "ident_cdr:app"]

EXPOSE 9988
