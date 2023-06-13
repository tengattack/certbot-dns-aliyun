# Aliyun DNS Authenticator plugin for Certbot

A certbot dns plugin to obtain certificates using aliyun.


## Obtain Aliyun RAM AccessKey
[https://ram.console.aliyun.com/](https://ram.console.aliyun.com/)

And ensure your RAM account has `AliyunDNSFullAccess` permission.

## Install

```bash
pip install certbot-dns-aliyun
```

For Snap:

```bash
sudo snap install certbot-dns-aliyun
sudo snap set certbot trust-plugin-with-root=ok
sudo snap connect certbot:plugin certbot-dns-aliyun
/snap/bin/certbot plugins
```

Or manually:

```bash
git clone https://github.com/tengattack/certbot-dns-aliyun
cd certbot-dns-aliyun
sudo python setup.py install
```

If you are using `certbot-auto`, you should run `virtualenv` first:

```bash
# CentOS 7
virtualenv --no-site-packages --python "python2.7" "/opt/eff.org/certbot/venv"
/opt/eff.org/certbot/venv/bin/python2.7 setup.py install
```

## Credentials File

```ini
dns_aliyun_access_key = 12345678
dns_aliyun_access_key_secret = 1234567890abcdef1234567890abcdef
```

```bash
chmod 600 /path/to/credentials.ini
```

## Obtain Certificates

```bash
certbot certonly \
    --authenticator=dns-aliyun \
    --dns-aliyun-credentials='/path/to/credentials.ini' \
    -d "*.example.com,example.com"
```

### Using Docker

Please refer to [scripts](./scripts/README.md)
