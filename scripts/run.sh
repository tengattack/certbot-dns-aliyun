#!/bin/bash

set -x

docker run -ti --rm \
    -v $(pwd)/credentials:/root/.secrets \
    -v $(pwd)/letsencrypt:/etc/letsencrypt \
    -v $(pwd)/nginx:/etc/nginx/conf.d \
    certbot/dns-aliyun \
    -c /etc/letsencrypt/cli.ini
