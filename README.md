# test-at-commands
Program for automatically testing AT commands

# installation
1. Download and extract the files to a directory
2. Navigate to the extracted directory
3. Satisfy the dependancies with:
```

pip install -r requirements.txt
```
4. Run the program with parameters:
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
# Example with ssh
1. Connect your device to the ethernet cable
2. In the configuration file **config.json** enter the device model with commands you want to test. In the data structure you need to specify what commands to run, the expected result and if there are any arguments to use (if not, then leave blank). An example of the data structure:

![image](https://user-images.githubusercontent.com/88384951/226345001-3c977585-76fc-4ef1-9894-f943ba515317.png)

4. Run the following command:
```
python3 main.py -d RUTX11 -c ssh --ip-address 192.168.1.1 -u root -P Admin123
```
5. You should be able to see what model is currently being tested and commands that are currently being tested. After the test it should show how many commands passed, how many commands failed and the total number of commands tested.
```
$ python3 main.py -d RUTX11 -c ssh --ip-address 192.168.1.1 -u root -P Admin123
Testing product: RUTX11
Currently testing: ATI
Currently testing: AT+CGMI
Currently testing: AT+CTZU=?
PASSED TESTS: 3
FAILED TESTS: 0
TOTAL TESTS: 3
```

7. After the test, the program should create a .csv file **MODEL_NAME_DATE.csv** with information: 

* about what command was tested;
* what result was expected;
* what was the result of the tested command and whether the command passed the test;
* the manufacturer and model of the modem.
