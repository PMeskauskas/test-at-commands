# test-at-commands
Program for automatically testing AT commands with serial/ssh protocols and an option to upload them to FTP server. 

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
usage: main.py [-h] -d--device-name D__DEVICE_NAME -c CONNECTION_TYPE [-p SERIAL_PORT] [--ip-address [IP_ADDRESS]]
               [-u [USERNAME]] [-P [PASSWORD]] [--enable_ftp [ENABLE_FTP]]

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
  --enable_ftp [ENABLE_FTP]
                        Option to upload to FTP server (True,False) (default: false)
```
# Example with ssh to send sms messages
1. Connect your device to the ethernet cable
2. In the configuration file **config.json** enter the device model with commands you want to test. In the data structure you need to specify what commands to run, the expected result, arguments and what extra commands to use (if arguments or extra commands not needed, then leave them blank). An example of the data structure is in **config.json**:

Configuration file command argument description:
* "command" argument is used to specify the running AT command without the argument, For example, AT+COPS.
* "argument" argument is used to specify the commands' arguments, for example, "1". You can also specify multiple arguments by seperating them with a comma, for example, if you input the command AT+COPS with arguments "help,1", the program will parse the command and the result will be "AT+COPS="help",1".
* "expected" argument is used to specify what the expected result should be, the program returns ERROR if the command failed and OK if the program succeded, so the expected argument should be "OK" or "ERROR".
* "extras" argument is used to specify extra inputs or commands to send to the modem after executing the main AT command. In this example we are sending "Sample text" and a SIGTSTP signal to the modem after sending AT+CMGS command.

![image](https://user-images.githubusercontent.com/88384951/226626282-28dc7688-afd7-46c3-a35d-6714b1b77cf7.png)


3. Run the following command:
```
python3 main.py -d RUTX11 -c ssh --ip-address 192.168.1.1 -u root -P Admin123
```
4. When testing you should be able to see what model is currently being tested, what commands  are currently being tested, command expected output, command actual output, how many tests currently passed or failed and the total number of tests.
```
Testing product: RUTX11
Currently testing: ATE1
Expected response: OK
Actual response: OK
PASSED TESTS: 1
FAILED TESTS: 0
TOTAL TESTS: 1
```

5. After the test, the program should create a .csv file **ModelName_Date.csv** with information: 
* the manufacturer and model of the modem;
* testing command number, test name, expected test output, actual test output and the status of the test;
* how many tests were passed;
* how many tests were failed;
* the total amount of tests.

![image](https://user-images.githubusercontent.com/88384951/226628110-0e1ddb5b-41d2-409c-8673-7fdbcf79c322.png)


