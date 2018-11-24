FROM certbot/certbot

COPY . src/certbot-dns-aliyun

RUN pip install --no-cache-dir --editable src/certbot-dns-aliyun
