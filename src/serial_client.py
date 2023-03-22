

def connect_to_server_with_serial(device):
    try:
        serial = __import__('serial')
        serial_client = serial.Serial(device['serial_port'],
                                      baudrate=115200,
                                      stopbits=serial.STOPBITS_ONE,
                                      bytesize=serial.EIGHTBITS,
                                      parity=serial.PARITY_NONE,
                                      timeout=0.5)
        return serial_client
    except TimeoutError:
        print(
            f"Was not able to connect with serial, PORT: {device['serial_port']}")
        exit(1)
    except serial.serialutil.SerialException:
        print(
            f"Could not open port with serial, PORT: {device['serial_port']} (Check permissions.)")
        exit(1)


def get_modem_manufacturer_with_serial(serial_client):
    manufacturer_dict = dict()
    manufacturer_commands = ['AT+GMI', "AT+GMM"]
    results = list()
    for i in range(0, len(manufacturer_commands)):
        while True:
            try:
                serial_client.write(f"{manufacturer_commands[i]}\r".encode())

                command_response = serial_client.read(
                    512).decode().replace('\n', ' ').split()[0]
                if command_response == '':
                    continue
                if command_response not in results:
                    results.insert(i, command_response)
                    break
            except:
                continue
    manufacturer_dict['manufacturer'] = {
        "manufacturer": results[0],
        'model': results[1],
    }
    return manufacturer_dict


def execute_extra_commands_with_serial(extra_commands, serial_client, time):
    for j in range(0, len(extra_commands)):
        time.sleep(0.5)
        if extra_commands[j]['command'].isnumeric():
            serial_client.write(
                f"{chr(int(extra_commands[j]['command']))}\r".encode())
        else:
            serial_client.write(
                f"{extra_commands[j]['command']}\r".encode())


def execute_at_commands_with_serial(commands, serial_client, device_name):
    print_commands = __import__("print_commands")
    curses = __import__('curses')
    time = __import__('time')

    stdscr = print_commands.init_stdscr(curses)
    command_results = get_modem_manufacturer_with_serial(serial_client)

    failed = 0
    passed = 0
    for i in range(0, len(commands)):
        while i+1 not in command_results:
            command = commands[i]['command']
            try:
                command = commands[i]['command']
                expected_response = commands[i]['expected']
                serial_client.write(f"{command}\r".encode())

                if 'extras' in commands[i]:
                    execute_extra_commands_with_serial(
                        commands[i]['extras'], serial_client, time)

                actual_response = serial_client.read(
                    1000).decode().replace('\n', ' ').split()[-1]

                if actual_response == '':
                    continue

                if actual_response == commands[i]['expected']:
                    status = 'Passed'
                    passed += 1
                else:
                    status = 'Failed'
                    failed += 1

                total_commands = passed+failed
                print_commands.print_at_commands(stdscr, curses, device_name, command, expected_response,
                                                 actual_response, passed, failed, total_commands)
                command_results[i+1] = {
                    "command": command, "expected": expected_response, 'actual': actual_response, "status": status
                }
                time.sleep(2)
            except:
                continue

    tests_dict = {"passed": passed,
                  "failed": failed, 'total': total_commands}
    command_results['tests'] = tests_dict
    serial_client.close()
    del serial_client
    print_commands.del_curses(curses)
    return command_results


def test_at_commands_with_serial(device):
    config_data = __import__("config_data")
    device_name = device['d__device_name']
    commands = config_data.get_at_commands(device_name)
    serial_client = connect_to_server_with_serial(device)
    serial_client.write(b"sudo systemctl stop ModemManager\r")
    command_results = execute_at_commands_with_serial(
        commands, serial_client, device_name)
    return command_results
