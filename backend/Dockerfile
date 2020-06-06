FROM python:3.6-slim

LABEL maintainer Nick <nick@night.com>

ARG env
ARG requirements_file
ENV REQUIREMENTS_FILE ${requirements_file:-dev.txt}

RUN apt-get update
RUN mkdir -p /usr/share/man/man1 /usr/share/man/man7

RUN apt-get install --upgrade -y bash curl
RUN apt-get install --upgrade -y g++ gcc make libffi-dev libssl-dev wget ffmpeg

RUN apt-get update
RUN apt-get install --upgrade -y python3 python3-dev python-dev python3-pip

ENV WAITFORIT_VERSION="v2.2.0"
RUN curl -o /usr/local/bin/waitforit -sSL https://github.com/maxcnunes/waitforit/releases/download/$WAITFORIT_VERSION/waitforit-linux_amd64 && \
    chmod +x /usr/local/bin/waitforit

ADD /requirements/base.txt /tmp
ADD /requirements/$REQUIREMENTS_FILE /tmp

RUN pip3 install --upgrade pip
RUN pip3 install -r /tmp/$REQUIREMENTS_FILE

ADD . /code/

RUN mkdir -p /data/logs
RUN mkdir -p /tmp/videos

VOLUME /data

EXPOSE 5000

WORKDIR /code/
