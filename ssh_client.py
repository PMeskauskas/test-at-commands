

def connect_to_server_with_ssh(device):
    try:
        paramiko = __import__('paramiko')
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=device['ip_address'],
                           username=device['username'],
                           password=device['password'],
                           timeout=10)
        # print(
        #    f"Successfully connected with ssh to {device['ip_address']}")
        return ssh_client
    except paramiko.AuthenticationException:
        print(f"Invalid authentication for: {device['ip_address']}")
        exit(1)
    except TimeoutError:
        print(
            f"Was not able to connect with SSH, IP: {device['ip_address']}")
        exit(1)
    except paramiko.SSHException:
        print(f"No existing session: {device['ip_address']}")
        exit(1)


def get_modem_manufacturer(channel):
    time = __import__('time')
    manufacturer_dict = dict()
    manufacturer_commands = ['AT+GMI', "AT+GMM"]
    results = list()
    while (len(results) != len(manufacturer_commands)):
        for i in range(0, len(manufacturer_commands)):
            channel.send(f"{manufacturer_commands[i]}\n")
            time.sleep(0.5)
            command_response = channel.recv(
                512).decode().replace('\n', ' ').split()[0]
            if command_response == '':
                continue
            if command_response not in results:
                results.insert(i, command_response)
    manufacturer_dict['manufacturer'] = {
        "manufacturer": results[0],
        'model': results[1],
    }
    return manufacturer_dict


def connect_to_channel(ssh_client):
    time = __import__("time")
    channel = ssh_client.invoke_shell()
    channel.recv(512)
    channel.send("/etc/init.d/gsmd stop\n")
    channel.recv(512)
    time.sleep(2)
    channel.send(
        "socat /dev/tty,raw,echo=0,escape=0x03 /dev/ttyUSB3,raw,setsid,sane,echo=0,nonblock ; stty sane\n")
    time.sleep(0.5)
    channel.recv(512)
    return channel


def print_at_commands(stdscr, curses, device_name, command, expected_response, actual_response, passed, failed, total_commands):
    stdscr.addstr(0, 0, f"Testing product: {device_name}")
    stdscr.addstr(1, 0, f"Currently testing: {command}")
    stdscr.addstr(2, 0,
                  f"Expected response: {expected_response}")

    stdscr.addstr(3, 0, f"Actual response: {actual_response}")
    stdscr.addstr(
        4, 0, f"PASSED TESTS: {passed}", curses.color_pair(1))
    stdscr.addstr(5, 0, f"FAILED TESTS: {failed}", curses.color_pair(2))
    stdscr.addstr(6, 0, f"TOTAL TESTS: {total_commands}")
    stdscr.refresh()
    stdscr.erase()


def test_at_commands_with_ssh(device):
    at_commands = __import__("at_commands")
    termcolor = __import__("termcolor")
    time = __import__('time')
    curses = __import__('curses')

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    commands = at_commands.get_at_commands(device['d__device_name'])
    device_name = device['d__device_name']

    ssh_client = connect_to_server_with_ssh(device)
    channel = connect_to_channel(ssh_client)
    command_results = get_modem_manufacturer(channel)

    failed = 0
    passed = 0
    for i in range(0, len(commands)):
        try:

            command = commands[i]['command']
            expected_response = commands[i]['expected']
            channel.send(f"{command}\n")

            actual_response = channel.recv(
                512).decode().replace('\n', ' ').split()[-1]

            if actual_response == expected_response:
                status = 'Passed'
                passed += 1
            else:
                status = 'Failed'
                failed += 1
            total_commands = passed+failed
            print_at_commands(stdscr, curses, device_name, command, expected_response,
                              actual_response, passed, failed, total_commands)
            command_results[i+1] = {
                "command": command, "expected": expected_response, 'actual': actual_response, "status": status
            }
            time.sleep(2)
        except:
            continue
    tests_dict = {"passed": passed, "failed": failed, 'total': total_commands}
    command_results['tests'] = tests_dict

    ssh_client.close()
    curses.echo()
    curses.nocbreak()
    curses.endwin()
    return command_results
