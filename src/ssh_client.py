from config_data import ConfigData
from print_commands import PrintCommands
import socket
import time
import paramiko


class SshClient:
    def __init__(self, device):

        self.device = device
        self.commands = ConfigData(
            self.device['d__device_name']).commands

        self.ssh_client = None
        self.channel = None
        self.command_results = dict()
        self.connect_to_server_with_ssh()
        self.connect_to_channel()
        self.get_modem_manufacturer_with_ssh()
        self.execute_at_commands_with_ssh()
        self.close_ssh()

    def connect_to_server_with_ssh(self):
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())
            self.ssh_client.connect(hostname=self.device['ip_address'],
                                    username=self.device['username'],
                                    password=self.device['password'],
                                    timeout=10)
        except paramiko.AuthenticationException:
            print(f"Invalid authentication for: {self.device['ip_address']}")
            exit(1)
        except TimeoutError:
            print(
                f"Was not able to connect with SSH, IP: {self.device['ip_address']}")
            exit(1)
        except paramiko.SSHException:
            print(f"No existing session: {self.device['ip_address']}")
            exit(1)

    def connect_to_channel(self):
        self.channel = self.ssh_client.invoke_shell()
        self.channel.settimeout(7)
        self.channel.recv(512)
        self.channel.send("/etc/init.d/gsmd stop\n")
        self.channel.recv(512)
        time.sleep(2)
        self.channel.send(
            "socat /dev/tty,raw,echo=0,escape=0x03 /dev/ttyUSB3,raw,setsid,sane,echo=0,nonblock ; stty sane\n")
        time.sleep(0.5)
        self.channel.recv(512)

    def get_modem_manufacturer_with_ssh(self):
        manufacturer_commands = ['AT+GMI', "AT+GMM"]
        results = list()
        while (len(results) != len(manufacturer_commands)):
            try:
                for i in range(0, len(manufacturer_commands)):
                    self.channel.send(f"{manufacturer_commands[i]}\n")
                    time.sleep(0.5)
                    command_list = self.channel.recv(
                        512).decode().replace('\n', ' ').split()
                    if command_list[0] == '':
                        continue
                    command_response = command_list[0]
                    if command_response == manufacturer_commands[i]:
                        command_response = command_list[1]
                    if command_response not in results:
                        results.insert(i, command_response)
                self.command_results['manufacturer'] = {
                    "manufacturer": results[0],
                    'model': results[1],
                }
            except socket.timeout:
                print("Lost connection to server with SSH")
                self.close_ssh()
                exit(1)

    def execute_at_commands_with_ssh(self):
        print_object = PrintCommands()

        failed = 0
        passed = 0
        total_commands = 0
        for i in range(0, len(self.commands)):
            try:
                command = self.commands[i]['command']
                expected_response = self.commands[i]['expected']

                self.channel.send(f"{command}\n")
                time.sleep(0.5)

                if 'extras' in self.commands[i]:
                    self.execute_extra_commands_with_ssh(
                        self.commands[i]['extras'])
                response = self.channel.recv(
                    1000).decode().replace('\n', ' ')
                while self.channel.recv_ready():
                    response += self.channel.recv(
                        1000).decode().replace('\n', ' ')
                actual_response = self.find_actual_response(response)
                if expected_response == actual_response:
                    status = 'Passed'
                    passed += 1
                else:
                    status = 'Failed'
                    failed += 1
                total_commands = passed+failed
                print_object.print_at_commands(self.device['d__device_name'], command, expected_response,
                                               actual_response, passed, failed, total_commands)
                self.command_results[i+1] = {
                    "command": command, "expected": expected_response, 'actual': actual_response, "status": status
                }
            except socket.timeout:
                tests_dict = {"passed": passed,
                              "failed": failed, 'total': total_commands}
                self.command_results['tests'] = tests_dict
                print_object.del_curses()
                print("Lost connection to server with SSH")
                self.close_ssh()
                return
            time.sleep(0.5)

        tests_dict = {"passed": passed,
                      "failed": failed, 'total': total_commands}
        self.command_results['tests'] = tests_dict
        print_object.del_curses()

    def execute_extra_commands_with_ssh(self, extra_commands):
        for j in range(0, len(extra_commands)):
            if extra_commands[j]['command'].isnumeric():
                self.channel.send(
                    f"{chr(int(extra_commands[j]['command']))}\n")
            else:
                self.channel.send(f"{extra_commands[j]['command']}\n")
            time.sleep(0.5)

    def find_actual_response(self, response):
        if 'ERROR' in response:
            return 'ERROR'
        if 'OK' in response:
            return 'OK'

    def close_ssh(self):
        self.ssh_client.close()
        self.channel.close()
