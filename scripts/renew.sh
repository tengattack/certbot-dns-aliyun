#!/bin/bash

set -x

service nginx stop

docker run -ti --rm \
    -v $(pwd)/credentials:/root/.secrets \
    -v $(pwd)/letsencrypt:/etc/letsencrypt \
    -v $(pwd)/nginx:/etc/nginx/conf.d \
    certbot/dns-aliyun \
    renew -q

service nginx start

service nginx status