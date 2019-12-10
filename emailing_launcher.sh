#!/bin/sh

cd /
cd home/pi/Dev/sensehat_env
sudo python send_email.py &
sudo python uploader.py &
cd /