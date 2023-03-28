import time
import serial
from config_data import ConfigData
from print_commands import PrintCommands


class SerialClient:
    def __init__(self, device):
        self.device = device
        self.commands = ConfigData(
            self.device['d__device_name']).commands
        self.serial_client = None
        self.command_results = dict()

        self.connect_to_server_with_serial()
        self.serial_client.write(b"sudo systemctl stop ModemManager\r")
        self.get_modem_manufacturer_with_serial()
        self.execute_at_commands_with_serial()
        self.close_serial()

    def connect_to_server_with_serial(self):
        try:

            self.serial_client = serial.Serial(self.device['serial_port'],
                                               baudrate=115200,
                                               stopbits=serial.STOPBITS_ONE,
                                               bytesize=serial.EIGHTBITS,
                                               parity=serial.PARITY_NONE,
                                               timeout=1,
                                               write_timeout=0.5)
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

    def get_modem_manufacturer_with_serial(self):
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
                        512).decode().replace('\n', ' ').split()

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

    def execute_at_commands_with_serial(self):

        print_object = PrintCommands()

        failed = 0
        passed = 0
        total_commands = 0
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
                    if current_time > 5:
                        raise TimeoutError
                    command = self.commands[i]['command']
                    expected_response = self.commands[i]['expected']
                    self.serial_client.write(f"{command}\r".encode())
                    if 'extras' in self.commands[i]:
                        self.execute_extra_commands_with_serial(
                            self.commands[i]['extras'])

                    actual_response = self.serial_client.read(
                        1000).decode().replace('\n', ' ').split()[-1]

                    if actual_response == '':
                        continue

                    if actual_response == self.commands[i]['expected']:
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

                except TimeoutError:
                    tests_dict = {"passed": passed,
                                  "failed": failed, 'total': total_commands}
                    self.command_results['tests'] = tests_dict
                    print_object.del_curses()
                    print("Lost connection with serial")
                    return
                except:
                    continue

        tests_dict = {"passed": passed,
                      "failed": failed, 'total': total_commands}
        self.command_results['tests'] = tests_dict
        print_object.del_curses()

    def execute_extra_commands_with_serial(self, extra_commands):
        for j in range(0, len(extra_commands)):
            time.sleep(0.5)
            if extra_commands[j]['command'].isnumeric():
                self.serial_client.write(
                    f"{chr(int(extra_commands[j]['command']))}\r".encode())
            else:
                self.serial_client.write(
                    f"{extra_commands[j]['command']}\r".encode())

    def close_serial(self):
        self.serial_client.close()
        del self.serial_client
