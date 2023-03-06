#!/bin/bash

set -x

docker run -ti --rm \
    -v /var/log/letsencrypt:/var/log/letsencrypt \
    -v $(pwd)/credentials:/root/.secrets \
    -v $(pwd)/letsencrypt:/etc/letsencrypt \
    -v $(pwd)/nginx:/etc/nginx/conf.d \
    certbot/dns-aliyun \
    renew -q

STATUS="$(systemctl is-active nginx.service)"
if [ "${STATUS}" = "active" ]; then
    nginx -s reload
else
    service nginx start
fi
