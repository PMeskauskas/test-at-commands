

def connect_to_server_with_serial(device):
    try:
        serial = __import__('serial')
        serial_client = serial.Serial(device['serial_port'],
                                      baudrate=115200,
                                      stopbits=serial.STOPBITS_ONE,
                                      bytesize=serial.EIGHTBITS,
                                      parity=serial.PARITY_NONE,
                                      timeout=0.3)
        # print(
        #   f"Successfully connected with serial to {device['serial_port']}")
        return serial_client
    except TimeoutError:
        print(
            f"Was not able to connect with serial, PORT: {device['serial_port']}")
        exit(1)
        pass
    except serial.serialutil.SerialException:
        print(
            f"Could not open port with serial, PORT: {device['serial_port']}")
        exit(1)


def get_modem_manufacturer_serial(serial_client):
    manufacturer_dict = dict()
    manufacturer_commands = ['AT+GMI', "AT+GMM"]
    results = list()
    while (len(results) != len(manufacturer_commands)):
        for i in range(0, len(manufacturer_commands)):
            try:
                serial_client.write(f"{manufacturer_commands[i]}\r".encode())
                command_response = serial_client.read(
                    512).decode().replace('\n', ' ').split()[1]
                print(command_response)
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
    time = __import__('time')
    curses = __import__('curses')
    commands = at_commands.get_at_commands(device['d__device_name'])
    device_name = device['d__device_name']
    stdscr = at_commands.init_stdscr(curses)
    serial_client = connect_to_server_with_serial(device)
    serial_client.write(b"sudo systemctl stop ModemManager\r")
    time.sleep(0.5)
    command_results = get_modem_manufacturer_serial(serial_client)
    failed = 0
    passed = 0
    while len(command_results) != len(commands)+1:
        for i in range(0, len(commands)):
            command = commands[i]['command']
            try:
                if i+1 in command_results:
                    continue
                command = commands[i]['command']
                expected_response = commands[i]['expected']
                serial_client.write(f"{command}\r".encode())
                actual_response = serial_client.read(
                    512).decode().replace('\n', ' ').split()[-1]

                if actual_response == '':
                    continue

                if actual_response == commands[i]['expected']:
                    status = 'Passed'
                    passed += 1
                else:
                    status = 'Failed'
                    failed += 1
                total_commands = passed+failed
                at_commands.print_at_commands(stdscr, curses, device_name, command, expected_response,
                                              actual_response, passed, failed, total_commands)
                command_results[i+1] = {
                    "command": command, "expected": expected_response, 'actual': actual_response, "status": status
                }
                time.sleep(2)
            except:
                continue

    tests_dict = {"passed": passed, "failed": failed, 'total': total_commands}
    command_results['tests'] = tests_dict
    serial_client.close()
    del serial_client
    at_commands.del_curses(curses)
    return command_results
