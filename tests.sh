#!/bin/sh
python3 main.py -d TRM240 -c serial -p /dev/ttyUSB2
python3 main.py -d RUT955 -c ssh --ip-address 192.168.1.1 -u root -P Admin123