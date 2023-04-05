import time
from src.command_printer import CommandPrinter
from src.csv_handler import CSVHandler


class TestHandler:
    def __init__(self, communication_client, device_name, commands):
        self.communication_client = communication_client
        self.csv_handler = CSVHandler()
        self.device_name = device_name
        self.command_results = dict()
        self.commands = commands
        self.model = None
        self.failed = 0
        self.passed = 0
        self.response = ""
        self.command = ""
        self.status = ""
        self.total_commands = 0
        self.expected_response = ""
        self.actual_response = ""

    def test_modem_manufacturer(self):
        manufacturer_commands = ['AT+GMI', "AT+GMM"]
        results = list()
        while (len(results) != len(manufacturer_commands)):
            try:
                for i in range(0, len(manufacturer_commands)):
                    self.response = self.communication_client.send_command_to_server(
                        f"{manufacturer_commands[i]}")
                    if self.response is None:
                        raise TimeoutError
                    print(self.response)
                    self.response = self.response.split()
                    command_response = self.response[0]
                    if command_response == manufacturer_commands[i]:
                        command_response = self.response[1]
                    if command_response not in results:
                        results.insert(i, command_response)
            except TimeoutError:
                self.communication_client.close_connection()
                self.csv_handler.close_csv_file()
                exit("Lost connection to server")
        manufacturer_results = {
            "manufacturer": results[0],
            'model': results[1],
        }
        self.model = results[1]
        self.csv_handler.write_manufacturer_data(manufacturer_results)

    def open_testing_session(self):
        self.communication_client.connect_to_server()
        self.communication_client.disable_modem_manager()
        self.csv_handler.create_csv_filename(self.device_name)
        self.csv_handler.open_csv_file()

    def close_testing_session(self):
        self.communication_client.enable_modem_manager()
        self.communication_client.close_connection()
        self.csv_handler.close_csv_file()

    def test_commands(self):
        command_printer = CommandPrinter()
        self.csv_handler.write_command_title()
        for i in range(0, len(self.commands)):
            try:
                self.command = self.commands[i]['command']
                self.expected_response = self.commands[i]['expected']
                self.response = self.communication_client.send_command_to_server(
                    f"{self.command}")
                self.execute_extra_commands(i)
                if self.response is None:
                    raise TimeoutError

                self.set_actual_response()
                self.check_if_actual_response_is_equal()
                self.total_commands = self.passed+self.failed
                self.set_command_result(i)
                command_printer.print_at_commands(self.command_results)
                self.csv_handler.write_command_data(self.command_results)
            except TimeoutError:
                command_printer.del_curses()
                self.csv_handler.write_test_results(self.command_results)
                print("Lost connection to server")
                return
            time.sleep(0.5)
        command_printer.del_curses()
        self.csv_handler.write_test_results(self.command_results)

    def execute_extra_commands(self, index):
        if 'extras' in self.commands[index]:
            extra_commands = self.commands[index]['extras']
            for j in range(0, len(extra_commands)):
                if extra_commands[j]['command'].isnumeric():
                    self.response = self.communication_client.send_command_to_server(
                        f"{chr(int(extra_commands[j]['command']))}")
                    if self.response is None:
                        return
                else:
                    self.response = self.communication_client.send_command_to_server(
                        f"{extra_commands[j]['command']}")
                    if self.response is None:
                        return

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
                'expected_response': self.expected_response,
                'actual_response': self.actual_response,
                'status': self.status,
                'passed': self.passed,
                'failed': self.failed,
                'total_commands': self.total_commands,
                'device_name': self.device_name,
                'model': self.model
            }
        except:
            print("Failed to set command result")
