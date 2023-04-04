import socket
import time
from command_printer import CommandPrinter


class TestHandler:
    def __init__(self, communication_client, device_name):
        self.communication_client = communication_client
        self.device_name = device_name
        self.command_results = dict()
        self.failed = 0
        self.passed = 0
        self.response = ""
        self.command = ""
        self.status = ""
        self.total_commands = 0
        self.expected_response = ""
        self.actual_response = ""
        self.tests_dict = ""

    def get_modem_manufacturer(self):
        manufacturer_commands = ['AT+GMI', "AT+GMM"]
        results = list()
        while (len(results) != len(manufacturer_commands)):
            try:
                for i in range(0, len(manufacturer_commands)):
                    response = self.communication_client.send_command_to_server(
                        f"{manufacturer_commands[i]}\n").split()
                    if response[0] == '':
                        continue
                    command_response = response[0]
                    if command_response == manufacturer_commands[i]:
                        command_response = response[1]
                    if command_response not in results:
                        results.insert(i, command_response)
            except socket.timeout:
                print("Lost connection to server with SSH")
                self.close_ssh()
                exit(1)
        manufacturer_results = {
            "manufacturer": results[0],
            'model': results[1],
        }
        print(manufacturer_results)
        return manufacturer_results

    def test_at_command(self, commands, command_printer):

        for i in range(0, len(self.commands)):
            try:
                self.command = commands[i]['command']
                self.expected_response = commands[i]['expected']
                self.channel.send(f"{self.command}\n")
                self.execute_extra_commands(i)
                self.get_response_from_channel()
                self.set_actual_response()
                self.check_if_actual_response_is_equal()
                self.total_commands = self.passed+self.failed
                command_printer.print_at_commands(self.device['d__device_name'], self.command, self.expected_response,
                                                  self.actual_response, self.passed, self.failed, self.total_commands)
                self.set_command_result()

            except socket.timeout:
                self.append_test_results()
                command_printer.del_curses()
                print("Lost connection to server with SSH")
                return
            time.sleep(0.5)
        self.append_test_results()

        command_printer.del_curses()

    def execute_extra_commands(self, command):
        if 'extras' in self.commands[index]:
            extra_commands = self.commands[index]['extras']
            for j in range(0, len(extra_commands)):
                if extra_commands[j]['command'].isnumeric():
                    self.channel.send(
                        f"{chr(int(extra_commands[j]['command']))}\n")
                else:
                    self.channel.send(f"{extra_commands[j]['command']}\n")
                time.sleep(0.5)

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

    def set_command_result(self, index):
        try:
            self.command_results = {
                'number': index,
                'command': self.command,
                'expected': self.expected_response,
                'actual': self.actual_response,
                'status': self.status
            }
        except:
            print("Failed to append result from command")

    def set_test_results(self):
        try:
            self.tests_dict = {'passed': self.passed,
                               'failed': self.failed,
                               'total': self.total_commands}
        except:
            print("Failed to append test results")
