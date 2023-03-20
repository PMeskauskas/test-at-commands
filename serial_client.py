import logging
import time


def connect_to_server_with_serial(device):
    try:
        serial = __import__('serial')
        serial_client = serial.Serial(device['serial_port'],
                                      baudrate=115200,
                                      stopbits=serial.STOPBITS_ONE,
                                      bytesize=serial.EIGHTBITS,
                                      parity=serial.PARITY_NONE,
                                      timeout=0.3)
        logging.info(
            f"Successfully connected with serial to {device['serial_port']}")
        return serial_client
    except TimeoutError:
        logging.error(
            f"Was not able to connect with serial, PORT: {device['serial_port']}")
        exit(1)
        pass
    except serial.serialutil.SerialException:
        logging.error(
            f"Could not open port with serial, PORT: {device['serial_port']}")
        exit(1)


def get_modem_manufacturer(serial_client):
    manufacturer_dict = dict()
    manufacturer_commands = ['AT+GMI', "AT+GMM"]
    results = list()
    while (len(results) != len(manufacturer_commands)):
        for i in range(0, len(manufacturer_commands)):
            try:
                serial_client.write(f"{manufacturer_commands[i]}\r".encode())
                command_response = serial_client.read(
                    512).decode().replace('\n', ' ').split()[0]
                if command_response == '':
                    continue
                if command_response not in results:
                    results.insert(i, command_response)
            except:
                continue
    manufacturer_dict['manufacturer'] = {
        "manufacturer": results[0],
        'model': results[1],
    }
    return manufacturer_dict


def test_at_commands_with_serial(device):
    at_commands = __import__("at_commands")
    commands = at_commands.get_at_commands(device['d__device_name'])
    serial_client = connect_to_server_with_serial(device)
    serial_client.write(b"sudo systemctl stop ModemManager\r")
    time.sleep(0.5)
    command_results = get_modem_manufacturer(serial_client)
    failed = 0
    passed = 0
    while len(command_results) != len(commands)+1:
        for i in range(0, len(commands)):
            command = commands[i]['command']
            try:
                if i+1 in command_results:
                    continue
                command = commands[i]['command']

                serial_client.write(f"{command}\r".encode())
                command_response = serial_client.read(512).decode()
                if command_response == '':
                    continue
                if "OK" in command_response:
                    status = 'Passed'
                    passed += 1
                else:
                    status = 'Failed'
                    failed += 1
                print(f"Currently testing: {command}")
                command_results[i+1] = {
                    "command": command, "status": status}
            except:
                continue
    tests_dict = {"passed": passed, "failed": failed, 'total': passed+failed}
    command_results['tests'] = tests_dict
    print(command_results)
    serial_client.close()
    del serial_client
    return command_results
