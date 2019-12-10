#!/bin/sh

cd /
cd home/pi/Dev/sensehat_env
sudo python3 send_email.py &
sudo python3 uploader.py &
cd /