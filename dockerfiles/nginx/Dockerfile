# vim: set syntax=dockerfile:

FROM nginx

MAINTAINER VNET a.s.

RUN rm /etc/nginx/conf.d/default.conf

COPY dockerfiles/nginx/app.nginx.conf \
  /etc/nginx/conf.d/default.conf
