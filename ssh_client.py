

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


def test_at_commands_with_ssh(device):
    at_commands = __import__("at_commands")
    termcolor = __import__("termcolor")
    time = __import__('time')
    commands = at_commands.get_at_commands(device['d__device_name'])
    print(f"Testing product: {device['d__device_name']}")
    ssh_client = connect_to_server_with_ssh(device)
    channel = ssh_client.invoke_shell()
    channel.recv(512)
    channel.send("/etc/init.d/gsmd stop\n")
    channel.recv(512)
    time.sleep(2)
    channel.send(
        "socat /dev/tty,raw,echo=0,escape=0x03 /dev/ttyUSB3,raw,setsid,sane,echo=0,nonblock ; stty sane\n")
    time.sleep(0.5)
    channel.recv(512)
    command_results = get_modem_manufacturer(channel)
    failed = 0
    passed = 0
    for i in range(0, len(commands)):
        try:
            command = commands[i]['command']
            print(f"Currently testing: {command}")
            channel.send(f"{command}\n")
            time.sleep(0.5)
            command_response = channel.recv(
                512).decode().replace('\n', ' ').split()
            command_response = ''.join(command_response)

            if command_response == commands[i]['expected']:
                status = 'Passed'
                passed += 1
            else:
                status = 'Failed'
                failed += 1

            command_results[i+1] = {
                "command": command, "status": status}
        except:
            continue
    total_commands = passed+failed
    tests_dict = {"passed": passed, "failed": failed, 'total': total_commands}
    command_results['tests'] = tests_dict
    print(f"PASSED TESTS: {termcolor.colored(passed,'green')}")
    print(f"FAILED TESTS: {termcolor.colored(failed,'red')}")
    print(f"TOTAL TESTS: {total_commands}")
    ssh_client.close()
    return command_results
