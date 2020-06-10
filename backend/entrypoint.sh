#!/bin/bash -e

printenv > /etc/cron.d/fetch-police-brutality-data-cron
echo "0 */2 * * * fetch-police-brutality-data >> /var/log/cron.log 2>&1" >> /etc/cron.d/fetch-police-brutality-data-cron
chmod +x /etc/cron.d/fetch-police-brutality-data-cron
crontab /etc/cron.d/fetch-police-brutality-data-cron
touch /var/log/cron.log
cron

exec "$@"
