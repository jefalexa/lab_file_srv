#!/bin/sh

echo "starting run.sh"
logger "starting run.sh"
pwd

/usr/sbin/cron
/usr/sbin/sshd -D

echo "run.sh complete"
logger "run.sh complete"
