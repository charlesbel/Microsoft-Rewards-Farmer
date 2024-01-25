#!/bin/bash

# Check if RUN_ONCE environment variable is set. In case, running the script now and exiting.
if [ "$RUN_ONCE" = "true" ]
then
    echo "RUN_ONCE environment variable is set. Running the script now and exiting."
    python main.py
    exit 0
fi
# Check if CRON_SCHEDULE environment variable is set
if [ -z "$CRON_SCHEDULE" ]
then
    echo "CRON_SCHEDULE environment variable is not set. Setting it to 4 AM everyday by default"
    CRON_SCHEDULE="0 4 * * *"
fi

# Setting up cron job
echo "$CRON_SCHEDULE root python /app/main.py >> /var/log/cron.log 2>&1" > /etc/cron.d/rewards-cron-job

# Give execution rights on the cron job
chmod 0644 /etc/cron.d/rewards-cron-job

# Apply cron job
crontab /etc/cron.d/rewards-cron-job

# Create the log file to be able to run tail
touch /var/log/cron.log

echo "Cron job is set to run at $CRON_SCHEDULE. Waiting for the cron to run..."

# Run the cron
cron && tail -f /var/log/cron.log
