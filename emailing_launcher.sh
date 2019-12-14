#!/bin/sh

cd /
cd home/pi/Dev/sensehat_env
sudo python3 send_email.py &
python3 uploader.py &
python3 scp_uploader.py &
cd /