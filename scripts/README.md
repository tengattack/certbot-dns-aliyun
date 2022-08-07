# Automation scripts

This folder provides some scripts for fetching the certs automatically.

## Prerequisites

* Docker
* nginx

## Usage

Edit the two configuration files:

* ./credentails/aliyun.ini
* ./letsencrypt/cli.ini

Then you can execute these scripts.

```shell
# Build the contailer locally.
./build.sh

# Generate some symbol links for convience and add a crontab job for renewal.
./setup.sh

# Setup the certbot manually for the first time.
./run.sh
```

Now you are set with automatic renewal!