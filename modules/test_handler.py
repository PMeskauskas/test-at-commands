import time
from modules.command_printer import CommandPrinter
from modules.csv_handler import CSVHandler
from modules.mail_sender import MailSender


class TestHandler:
    def __init__(self, communication_client, email, device_name, commands):
        self.communication_client = communication_client
        self.csv_handler = CSVHandler()
        self.mail_sender = MailSender()
        self.device_name = device_name
        self.email = email
        self.command_results = dict()
        self.commands = commands
        self.model = None
        self.failed_command_count = 0
        self.passed_command_count = 0
        self.total_command_count = 0
        self.response = ""
        self.command = ""
        self.response_status = ""
        self.expected_response = ""
        self.actual_response = ""

    def test_modem_manufacturer(self):
        manufacturer_commands = ['AT+GMI', "AT+GMM"]
        results = list()
        for i in range(0, len(manufacturer_commands)):
            try:
                self.response = self.communication_client.execute_at_command(
                    f"{manufacturer_commands[i]}")
                self.response = self.response.split()
                command_response = self.response[0]
                if command_response == manufacturer_commands[i]:
                    command_response = self.response[1]
                if command_response not in results:
                    results.insert(i, command_response)
            except TimeoutError:
                self.communication_client.close_connection()
                self.csv_handler.close_csv_file()
                self.mail_sender.form_message_failed(
                    destination=self.email, device_name=self.device_name)
                self.mail_sender.send_mail()
                exit("Lost connection to server")
        manufacturer_results = {
            "manufacturer": results[0],
            'model': results[1],
        }
        self.model = results[1]
        self.csv_handler.write_manufacturer_data(manufacturer_results)

    def open_testing_session(self):
        try:
            self.communication_client.connect_to_server()
            self.communication_client.disable_modem_manager()
            self.csv_handler.create_csv_filename(self.device_name)
            self.csv_handler.open_csv_file()
        except TimeoutError:
            pass

    def close_testing_session(self):
        try:
            self.communication_client.enable_modem_manager()
            self.communication_client.close_connection()
            self.csv_handler.close_csv_file()
        except TimeoutError:
            pass

    def test_commands(self):
        command_printer = CommandPrinter()
        self.csv_handler.write_command_title()
        for i in range(0, len(self.commands)):
            try:
                self.command = self.commands[i]['command']
                self.expected_response = self.commands[i]['expected']
                self.response = self.communication_client.execute_at_command(
                    f"{self.command}")
                self.execute_extra_commands(i)
                self.set_actual_response()
                self.check_if_actual_response_is_equal()
                self.total_command_count = self.passed_command_count+self.failed_command_count
                self.set_command_result(i+1)
                command_printer.print_at_commands(self.command_results)
                self.csv_handler.write_command_data(self.command_results)
            except TimeoutError:
                command_printer.del_curses()
                self.csv_handler.write_test_results(self.command_results)
                command_printer.print_at_command_to_terminal(
                    self.command_results)
                self.mail_sender.form_message_failed(
                    destination=self.email, device_name=self.device_name)
                self.mail_sender.send_mail()
                print("Lost connection to server")
                raise TimeoutError
        command_printer.del_curses()
        command_printer.print_at_command_to_terminal(self.command_results)
        self.csv_handler.write_test_results(self.command_results)
        self.mail_sender.form_message_success(
            destination=self.email, device_name=self.device_name)
        self.mail_sender.send_mail()

    def execute_extra_commands(self, index):
        if 'extras' in self.commands[index]:
            extra_commands = self.commands[index]['extras']
            for j in range(0, len(extra_commands)):
                if extra_commands[j]['command'].isnumeric():
                    self.response = self.communication_client.execute_at_command(
                        f"{chr(int(extra_commands[j]['command']))}")
                    if self.response is None:
                        return
                else:
                    self.response = self.communication_client.execute_at_command(
                        f"{extra_commands[j]['command']}")
                    if self.response is None:
                        return

    def set_actual_response(self):
        if self.response is None:
            self.actual_response = 'ERROR'
            return
        if 'ERROR' in self.response:
            self.actual_response = 'ERROR'
            return
        if 'OK' in self.response:
            self.actual_response = 'OK'
            return

    def check_if_actual_response_is_equal(self):
        if self.expected_response == self.actual_response:
            self.response_status = 'Passed'
            self.passed_command_count += 1
        else:
            self.response_status = 'Failed'
            self.failed_command_count += 1

    def set_command_result(self, index):
        try:
            self.command_results = {
                'number': index,
                'command': self.command,
                'expected_response': self.expected_response,
                'actual_response': self.actual_response,
                'response_status': self.response_status,
                'passed_command_count': self.passed_command_count,
                'failed_command_count': self.failed_command_count,
                'total_command_count': self.total_command_count,
                'device_name': self.device_name,
                'model': self.model
            }
        except:
            print("Failed to set command result")
