FROM certbot/certbot

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && \
        apk update && apk add nginx && mkdir -p /var/run/nginx

COPY . src/certbot-dns-aliyun

RUN pip install -i https://mirrors.aliyun.com/pypi/simple \
            certbot-nginx && \
        pip install -i https://mirrors.aliyun.com/pypi/simple \
            --no-cache-dir --editable src/certbot-dns-aliyun