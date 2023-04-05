import time
import serial
import subprocess


class CommunicationClient:
    def __init__(self, *args, **kwargs):
        self.serial_client = None
        self.serial_port = kwargs['serial_port']

    def connect_to_server(self):
        try:
            self.serial_client = serial.Serial(self.serial_port,
                                               baudrate=115200,
                                               stopbits=serial.STOPBITS_ONE,
                                               bytesize=serial.EIGHTBITS,
                                               parity=serial.PARITY_NONE,
                                               timeout=0.5)
        except TimeoutError:
            exit(
                f"Was not able to connect with serial, PORT: {self.serial_port}")

        except serial.SerialException:
            exit(
                f"Could not open port with serial, PORT: {self.serial_port} (Check permissions)")

        except:
            exit(
                f"Error when connecting with serial")

    def disable_modem_manager(self):
        try:
            subprocess.run(b"systemctl stop ModemManager",
                           shell=True, check=True)
        except:
            self.close_connection()
            exit("Failed to disable modem manager (Check permissions)")

    def enable_modem_manager(self):
        try:
            subprocess.run(b"systemctl start ModemManager",
                           shell=True, check=True)
        except:
            self.close_connection()
            exit("Failed to enable modem manager (Check permissions)")

    def send_command_to_server(self, command):
        response = ''
        attempts = 0
        start_time = time.time()
        while True:
            try:
                attempts+1
                current_time = time.time() - start_time
                attempts += 1
                if attempts > 50 or current_time > 7:
                    raise TimeoutError
                self.serial_client.write(
                    f"{command}\r".encode())

                response = self.serial_client.read(
                    20480).decode().replace('\n', ' ')

                if response == '':
                    continue
                return response
            except TimeoutError:
                return None
            except:
                continue

    def close_connection(self):
        self.serial_client.close()
        del self.serial_client
