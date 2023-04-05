import sys
from src.argument_parser import ArgumentParser
from src.config_handler import ConfigHandler
from src.communication_handler import CommunicationHandler
from src.ftp_uploader import FTPUploader
from src.test_handler import TestHandler

argument_parser = None
config_handler = None
test_handler = None
ftp_uploader = None


def init_modules():
    global argument_parser, config_handler, communication_handler, test_handler, ftp_uploader
    argument_parser = ArgumentParser()
    parse_arguments()
    config_handler = ConfigHandler('config.json')
    get_configuration_data()
    communication_handler = CommunicationHandler(
        f"{argument_parser.arguments['connection_type']}_client", **argument_parser.arguments)
    test_handler = TestHandler(
        communication_handler, argument_parser.arguments['d__device_name'], config_handler.commands)

    if argument_parser.arguments['enable_ftp']:
        ftp_uploader = FTPUploader()


def parse_arguments():
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


def test_commands():
    test_handler.open_testing_session()
    test_handler.test_modem_manufacturer()
    test_handler.test_commands()
    test_handler.close_testing_session()


def upload_file_to_ftp_server():
    ftp_uploader.open_ftp_session(config_handler.ftp_server_data)
    ftp_uploader.open_ftp_file(test_handler.csv_handler.filename)
    ftp_uploader.store_ftp_file(test_handler.csv_handler.filename)
    ftp_uploader.close_ftp()


def main():
    sys.path.append('src')
    init_modules()
    get_configuration_data()
    test_commands()
    if argument_parser.arguments['enable_ftp']:
        upload_file_to_ftp_server()


if __name__ == '__main__':
    main()
