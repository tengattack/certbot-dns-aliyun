FROM certbot/certbot:v2.3.0

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && \
        apk update && apk add nginx && mkdir -p /var/run/nginx

COPY . src/certbot-dns-aliyun

RUN pip install -i https://mirrors.aliyun.com/pypi/simple -r src/certbot-dns-aliyun/requirements.txt && \
        pip install -i https://mirrors.aliyun.com/pypi/simple \
            --no-cache-dir --editable src/certbot-dns-aliyun
