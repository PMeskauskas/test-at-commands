import time
import serial
from command_printer import PrintCommands


class CommunicationClient:
    def __init__(self, device, commands, *args, **kwargs):
        self.device = device
        self.commands = commands
        self.serial_client = None
        self.command_results = dict()
        self.failed = 0
        self.passed = 0
        self.response = ""
        self.command = ""
        self.status = ""
        self.total_commands = 0
        self.expected_response = ""
        self.actual_response = ""

    def connect_to_server(self):
        try:

            self.serial_client = serial.Serial(self.device['serial_port'],
                                               baudrate=115200,
                                               stopbits=serial.STOPBITS_ONE,
                                               bytesize=serial.EIGHTBITS,
                                               parity=serial.PARITY_NONE,
                                               timeout=0.5)
        except TimeoutError:
            print(
                f"Was not able to connect with serial, PORT: {self.device['serial_port']}")
            exit(1)
        except serial.SerialException:
            print(
                f"Could not open port with serial, PORT: {self.device['serial_port']} (Check permissions.)")
            exit(1)
        except:
            print(
                f"Error when connecting with serial")
            exit(1)

    def disable_modem_manager(self):
        try:
            self.serial_client.write(b"systemctl stop ModemManager\r")
        except:
            print("Failed to disable modem manager")
            self.close_serial()
            exit(1)

    def enable_modem_manager(self):
        try:

            self.serial_client.write(b"systemctl start ModemManager\r")
        except:
            print("Failed to enable modem manager")
            self.close_serial()
            exit(1)

    def get_modem_manufacturer(self):
        manufacturer_commands = ['AT+GMI', "AT+GMM"]
        results = list()

        for i in range(0, len(manufacturer_commands)):
            attempts = 0
            while True:
                try:
                    attempts+1
                    if attempts > 50:
                        raise TimeoutError
                    self.serial_client.write(
                        f"{manufacturer_commands[i]}\r".encode())

                    command_list = self.serial_client.read(
                        20480).decode().replace('\n', ' ').split()

                    if command_list[0] == '':
                        continue
                    command_response = command_list[0]
                    if command_response == manufacturer_commands[i]:
                        command_response = command_list[1]

                    if command_response not in results:
                        results.insert(i, command_response)
                        break

                except TimeoutError:
                    self.close_serial()
                    print("Lost connection with serial")
                    exit(1)
                except:
                    continue
        self.command_results['manufacturer'] = {
            "manufacturer": results[0],
            'model': results[1],
        }

    def test_command(self):

        print_object = PrintCommands()

        for i in range(0, len(self.commands)):
            attempts = 0
            start_time = time.time()
            while i+1 not in self.command_results:
                command = self.commands[i]['command']
                try:
                    current_time = time.time() - start_time
                    attempts += 1
                    if attempts > 50:
                        raise TimeoutError
                    if current_time > 10:
                        raise TimeoutError
                    self.command = self.commands[i]['command']
                    self.expected_response = self.commands[i]['expected']
                    self.serial_client.write(f"{command}\r".encode())
                    if 'extras' in self.commands[i]:
                        self.execute_extra_commands_with_serial(
                            self.commands[i]['extras'])

                    self.response = self.serial_client.read(
                        20480).decode().replace('\n', ' ')
                    if self.response == '':
                        continue

                    self.set_actual_response()
                    self.check_if_actual_response_is_equal()
                    self.total_commands = self.passed + self.failed

                    print_object.print_at_commands(self.device['d__device_name'], command, self.expected_response,
                                                   self.actual_response, self.passed, self.failed, self.total_commands)
                    self.append_command_result(i+1)

                except TimeoutError:
                    self.append_test_results()
                    print_object.del_curses()
                    print("Lost connection with serial")
                    return
                except:
                    continue

        self.append_test_results()
        print_object.del_curses()

    def test_extra_commands(self, extra_commands):
        for j in range(0, len(extra_commands)):
            time.sleep(0.5)
            if extra_commands[j]['command'].isnumeric():
                self.serial_client.write(
                    f"{chr(int(extra_commands[j]['command']))}\r".encode())
            else:
                self.serial_client.write(
                    f"{extra_commands[j]['command']}\r".encode())

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
            print("Failed to append test results")

    def close(self):
        self.serial_client.close()
        del self.serial_client
