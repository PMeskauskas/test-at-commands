# test-at-commands
Program for automatically testing AT commands

# installation
1. Download and extract the files to a directory
2. Navigate to the extracted directory
3. Satisfy the dependancies with:
```

pip install -r requirements.txt
```
4. Run the program with parameters
```
$ sudo python3 main.py -h
usage: main.py [-h] -d--device-name D__DEVICE_NAME -c CONNECTION_TYPE [-p SERIAL_PORT] [--ip-address [IP_ADDRESS]] [-u [USERNAME]] [-P [PASSWORD]]

Program to automatically test AT commands

options:
  -h, --help            show this help message and exit
  -d--device-name D__DEVICE_NAME
                        Device name (for example: RUTX11, TRM240) (default: None)
  -c CONNECTION_TYPE, --connection-type CONNECTION_TYPE
                        Connection type (ssh, serial) (default: None)
  -p SERIAL_PORT, --serial-port SERIAL_PORT
                        Serial usb port (default: /dev/ttyUSB2)
  --ip-address [IP_ADDRESS]
                        Server IP address (default: 192.168.1.1)
  -u [USERNAME], --username [USERNAME]
                        Server username (default: root)
  -P [PASSWORD], --password [PASSWORD]
                        Server password (default: Admin123)
```
# Example
