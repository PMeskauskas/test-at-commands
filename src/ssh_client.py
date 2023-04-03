from print_commands import PrintCommands
import socket
import time
import paramiko


class SshClient:
    def __init__(self, device, commands, *args, **kwargs):
        self.device = device
        self.commands = commands
        self.ssh_client = None
        self.channel = None
        self.command_results = dict()
        self.failed = 0
        self.passed = 0
        self.response = ""
        self.command = ""
        self.status = ""
        self.total_commands = 0
        self.expected_response = ""
        self.actual_response = ""

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
        time.sleep(0.5)

    def disable_modem_manager(self):
        try:
            self.channel.send("/etc/init.d/gsmd stop\n")
            self.get_response_from_channel()
            time.sleep(1)
        except:
            print("Failed to disable modem manager")
            self.close_ssh()
            exit(1)

    def enable_modem_manager(self):
        try:
            self.channel.send("/etc/init.d/gsmd start\n")
            time.sleep(1)
        except:
            print("Failed to enable modem manager")
            self.close_ssh()
            exit(1)

    def enable_at_commands(self):
        try:
            self.channel.send(
                "socat /dev/tty,raw,echo=0,escape=0x03 /dev/ttyUSB3,raw,setsid,sane,echo=0,nonblock ; stty sane\n")
            time.sleep(1)
            self.get_response_from_channel()
        except:
            print("Failed to enable at commands")
            self.close_ssh()
            exit(1)

    def get_modem_manufacturer_with_ssh(self):
        manufacturer_commands = ['AT+GMI', "AT+GMM"]
        results = list()
        while (len(results) != len(manufacturer_commands)):
            try:
                for i in range(0, len(manufacturer_commands)):
                    self.channel.send(f"{manufacturer_commands[i]}\n")
                    time.sleep(0.5)

                    self.get_response_from_channel()
                    self.response = self.response.split()
                    if self.response[0] == '':
                        continue
                    command_response = self.response[0]
                    if command_response == manufacturer_commands[i]:
                        command_response = self.response[1]
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

        for i in range(0, len(self.commands)):
            try:
                self.command = self.commands[i]['command']
                self.expected_response = self.commands[i]['expected']
                self.channel.send(f"{self.command}\n")
                time.sleep(0.5)
                self.execute_extra_commands_with_ssh(i)
                self.get_response_from_channel()
                self.set_actual_response()
                self.check_if_actual_response_is_equal()
                self.total_commands = self.passed+self.failed
                print_object.print_at_commands(self.device['d__device_name'], self.command, self.expected_response,
                                               self.actual_response, self.passed, self.failed, self.total_commands)
                self.append_command_result(i+1)

            except socket.timeout:
                self.append_test_results()
                print_object.del_curses()
                print("Lost connection to server with SSH")
                self.close_ssh()
                return
            time.sleep(0.5)
        self.append_test_results()

        print_object.del_curses()

    def execute_extra_commands_with_ssh(self, index):
        if 'extras' in self.commands[index]:
            extra_commands = self.commands[index]['extras']
            for j in range(0, len(extra_commands)):
                if extra_commands[j]['command'].isnumeric():
                    self.channel.send(
                        f"{chr(int(extra_commands[j]['command']))}\n")
                else:
                    self.channel.send(f"{extra_commands[j]['command']}\n")
                time.sleep(0.5)

    def get_response_from_channel(self):
        self.response = self.channel.recv(
            1000).decode().replace('\n', ' ')
        while self.channel.recv_ready():
            self.response += self.channel.recv(
                1000).decode().replace('\n', ' ')

    def set_actual_response(self):
        if 'ERROR' in self.response:
            self.actual_response = 'ERROR'
        if 'OK' in self.response:
            self.actual_response = 'OK'

    def check_if_actual_response_is_equal(self):
        if self.expected_response == self.actual_response:
            self.status = 'Passed'
            self.passed += 1
        else:
            self.status = 'Failed'
            self.failed += 1

    def append_command_result(self, index):
        try:
            self.command_results[index] = {
                'command': self.command,
                'expected': self.expected_response,
                'actual': self.actual_response,
                'status': self.status
            }
        except:
            print("Failed to append result from command")

    def append_test_results(self):
        try:
            tests_dict = {'passed': self.passed,
                          'failed': self.failed,
                          'total': self.total_commands}
            self.command_results['tests'] = tests_dict
        except:
            print("Failed to append results from command")

    def close_ssh(self):
        self.ssh_client.close()
        self.channel.close()
