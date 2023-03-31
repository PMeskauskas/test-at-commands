#!/bin/sh
python3 main.py -d TRM240 -c serial -p /dev/ttyUSB2 --enable_ftp true
python3 main.py -d RUTX11 -c ssh --ip-address 192.168.1.1 -u root -P Admin123 --enable_ftp true