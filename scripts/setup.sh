#!/bin/bash

set -x

ln -s $(pwd)/letsencrypt /etc/letsencrypt

# Optional, add a symbol link to the real nginx configuration folder may cause some problems,
# since the certbot sometimes could not update the entries correctly.
# You'd better to update your real nginx configuration file manually.
# ln -s $(pwd)/nginx /etc/nginx/conf.d

# Install crontab job
RENEW_SH="$(pwd)/renew.sh"
SLEEPTIME=$(awk 'BEGIN{srand(); print int(rand()*(3600+1))}')

echo "0 0,12 * * * root sleep $SLEEPTIME && $RENEW_SH" | tee -a /etc/crontab > /dev/null
