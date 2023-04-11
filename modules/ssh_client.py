import socket
import time
import paramiko


class CommunicationClient:
    def __init__(self, *args, **kwargs):
        self.addr = kwargs['ip_address']
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.ssh_client = None
        self.channel = None

    def connect_to_server(self):
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())
            self.ssh_client.connect(hostname=self.addr,
                                    username=self.username,
                                    password=self.password,
                                    timeout=5)
            self.connect_to_channel()

        except paramiko.AuthenticationException:
            exit(f"Invalid authentication for: {self.addr}")
        except TimeoutError:
            exit(
                f"Was not able to connect with SSH, IP: {self.addr}")
        except paramiko.SSHException:
            exit(f"No existing session: {self.addr}")

    def connect_to_channel(self):
        self.channel = self.ssh_client.invoke_shell()
        self.channel.settimeout(7)
        time.sleep(0.5)

    def disable_modem_manager(self):
        self.execute_at_command(
            "/etc/init.d/gsmd stop\n")
        self.execute_at_command(
            "socat /dev/tty,raw,echo=0,escape=0x03 /dev/ttyUSB3,raw,setsid,sane,echo=0,nonblock ; stty sane\n")

    def enable_modem_manager(self):

        self.execute_at_command(f"{chr(int(3))}\n")
        time.sleep(2)
        i = 0
        while i < 3:
            i += 1
            self.execute_at_command(
                "/etc/init.d/gsmd start\n")

    def execute_at_command(self, command):
        try:
            self.channel.send(f"{command}\n")
            time.sleep(1)
            return self.get_response_from_channel()

        except socket.timeout:
            raise TimeoutError

    def get_response_from_channel(self):
        response = self.channel.recv(
            1000).decode().replace('\n', ' ')
        while self.channel.recv_ready():
            response += self.channel.recv(
                1000).decode().replace('\n', ' ')
        return response

    def close_connection(self):
        self.ssh_client.close()
        self.channel.close()
