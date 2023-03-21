# test-at-commands
Program for automatically testing AT commands with serial or ssh protocols

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
# Example with ssh to send sms messages
1. Connect your device to the ethernet cable
2. In the configuration file **config.json** enter the device model with commands you want to test. In the data structure you need to specify what commands to run, the expected result, arguments and what extra commands to use (if arguments or extra commands not needed, then leave blank). An example of the data structure in **config.json**:

![image](https://user-images.githubusercontent.com/88384951/226626282-28dc7688-afd7-46c3-a35d-6714b1b77cf7.png)


3. Run the following command:
```
python3 main.py -d RUTX11 -c ssh --ip-address 192.168.1.1 -u root -P Admin123
```
4. When testing you should be able to see what model is currently being tested, what commands  are currently being tested, command expected output, command actual output, how many tests currently passed or failed and the total number of tests.
```
$ python3 main.py -d RUTX11 -c ssh --ip-address 192.168.1.1 -u root -P Admin123
Testing product: RUTX11
Currently testing: AT+GM
Expected response: ERROR
Actual response: ERROR
PASSED TESTS: 2
FAILED TESTS: 0
TOTAL TESTS: 2
```

5. After the test, the program should create a .csv file **ModelName_Date.csv** with information: 
* the manufacturer and model of the modem;
* testing command number, test name, expected test output, actual test output and the status of the test;
* how many tests were passed;
* how many tests were failed;
* the total amount of tests.

![image](https://user-images.githubusercontent.com/88384951/226536551-0be88176-9538-4b7b-8dbf-23128a4b7b00.png)

