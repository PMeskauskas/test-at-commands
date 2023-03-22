

def connect_to_server_with_ssh(device):
    try:
        paramiko = __import__('paramiko')
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=device['ip_address'],
                           username=device['username'],
                           password=device['password'],
                           timeout=10)

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


def get_modem_manufacturer_with_ssh(channel):
    time = __import__('time')
    manufacturer_dict = dict()
    manufacturer_commands = ['AT+GMI', "AT+GMM"]
    results = list()
    while (len(results) != len(manufacturer_commands)):
        try:
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
        except:
            continue
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


def execute_extra_commands_with_ssh(extra_commands, channel, time):
    for j in range(0, len(extra_commands)):
        if extra_commands[j]['command'].isnumeric():
            channel.send(f"{chr(int(extra_commands[j]['command']))}\n")
        else:
            channel.send(f"{extra_commands[j]['command']}\n")
        time.sleep(0.5)


def execute_at_commands_with_ssh(commands, channel, device_name):
    print_commands = __import__("print_commands")
    curses = __import__('curses')
    time = __import__('time')
    stdscr = print_commands.init_stdscr(curses)
    command_results = get_modem_manufacturer_with_ssh(channel)
    failed = 0
    passed = 0
    for i in range(0, len(commands)):
        try:
            command = commands[i]['command']
            expected_response = commands[i]['expected']

            channel.send(f"{command}\n")
            time.sleep(0.5)

            if 'extras' in commands[i]:
                execute_extra_commands_with_ssh(
                    commands[i]['extras'], channel, time)

            actual_response = channel.recv(
                512).decode().replace('\n', ' ').split()[-1]
            if actual_response == expected_response:
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
    tests_dict = {"passed": passed, "failed": failed, 'total': total_commands}
    command_results['tests'] = tests_dict
    print_commands.del_curses(curses)
    return command_results


def test_at_commands_with_ssh(device):
    config_data = __import__("config_data")
    device_name = device['d__device_name']

    commands = config_data.get_at_commands(device_name)
    ssh_client = connect_to_server_with_ssh(device)
    channel = connect_to_channel(ssh_client)
    command_results = execute_at_commands_with_ssh(
        commands, channel, device_name)

    ssh_client.close()
    channel.close()

    return command_results
