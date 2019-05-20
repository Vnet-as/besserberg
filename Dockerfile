# vim: set syntax=dockerfile:

FROM python:3.7

LABEL maintainer "VNET a.s. <db@vnet.sk>"

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
 && apt-get install -y \
    xvfb \
    ghostscript \
    ttf-dejavu \
    libssl1.0-dev \
 && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

ADD /vendor/wkhtmltopdf.tar.xz /usr/bin
COPY ./wkhtmltopdf.sh /usr/bin/wkhtmltopdf.sh
RUN chmod a+x /usr/bin/wkhtmltopdf.sh

COPY ./besserberg /opt/besserberg
WORKDIR /opt/besserberg

ENV PYTHONPATH /opt:$PYTHONPATH

EXPOSE 8000

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "besserberg.app:app"]
