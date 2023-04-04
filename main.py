import sys
from src.argument_parser import ArgumentParser
from src.config_handler import ConfigHandler
from src.communication_handler import CommunicationHandler
from src.csv_handler import CSVHandler
from src.ftp_uploader import FTPUploader
from src.test_handler import TestHandler
from src.command_printer import CommandPrinter

argument_parser = None
config_handler = None
communication_handler = None
csv_handler = None
command_printer = None
test_handler = None
ftp_uploader = None


def init_modules():
    global argument_parser, config_handler, communication_handler, test_handler, command_printer, csv_handler, ftp_uploader
    argument_parser = ArgumentParser()
    parse_arguments()
    config_handler = ConfigHandler('config.json')
    communication_handler = CommunicationHandler(
        f"{argument_parser.arguments['connection_type']}_client", **argument_parser.arguments)
    test_handler = TestHandler(
        communication_handler, argument_parser.arguments['d__device_name'])
    command_printer = CommandPrinter()
    csv_handler = CSVHandler()
    if argument_parser.arguments['enable_ftp']:
        ftp_uploader = FTPUploader()


def parse_arguments():
    global argument_parser
    argument_parser.parse_arguments()
    argument_parser.adjust_case_sensitivity()
    argument_parser.check_connectivity()
    argument_parser.check_upload_to_ftp()


def get_configuration_data():
    config_handler.open_configuration_file()
    config_handler.load_configuration_data()
    config_handler.get_commands_by_device_name(
        argument_parser.arguments['d__device_name'])
    config_handler.parse_device_configuration_data()
    if argument_parser.arguments['enable_ftp']:
        config_handler.get_ftp_server_data()
    config_handler.close_configuration_file()


def open_testing_session():
    test_handler.communication_client.connect_to_server()
    test_handler.communication_client.disable_modem_manager()
    csv_handler.create_csv_filename(
        argument_parser.arguments['d__device_name'])
    csv_handler.open_csv_file()


def execute_modem_commands():
    manufacturer_data = test_handler.get_modem_manufacturer()
    csv_handler.write_manufacturer_data(manufacturer_data)
    exit()


def test_commands():
    commands = config_handler.commands
    pass


def close_testing_session():
    global test_handler, csv_handler
    test_handler.communication_client.execute_at_commands()
    test_handler.communication_client.enable_modem_manager()
    test_handler.communication_client.close_serial()
    csv_handler.close_csv_file()


def print_command_results_to_csv():

    csv_handler.write_to_csv_file()


def upload_file_to_ftp_server(filename, hostname, username, password):
    ftp_uploader.open_ftp_session(hostname, username, password)
    ftp_uploader.open_ftp_file(filename)
    ftp_uploader.store_ftp_file(filename)
    ftp_uploader.close_ftp()


def main():
    sys.path.append('src')
    init_modules()
    get_configuration_data()
    open_testing_session()
    execute_modem_commands()
    test_commands()
    close_testing_session()
    if argument_parser.arguments['enable_ftp']:
        upload_file_to_ftp_server(csv_handler.filename,)


if __name__ == '__main__':
    main()
