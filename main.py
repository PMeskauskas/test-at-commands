from src.argument_parser import ArgumentParser
from src.print_results import PrintResults
from src.ftp_upload import FTPUpload
from src.config_data import ConfigData
import sys


def get_arguments():
    args = ArgumentParser()
    args.parse_arguments()
    args.adjust_case_sensitivity()
    args.check_connectivity()
    args.check_upload_to_ftp()
    return args.arguments


def get_configuration_data(device_name, enable_ftp):
    config_object = ConfigData('config.json')
    config_object.open_configuration_file()
    config_object.load_configuration_data()
    config_object.get_commands_by_device_name(device_name)
    config_object.parse_device_configuration_data()
    if enable_ftp:
        config_object.get_ftp_server_data()
    config_object.config_file.close()
    return config_object


def get_command_results_with_ssh(args, commands):
    ssh_client = __import__('ssh_client')
    ssh_object = ssh_client.SshClient(args, commands)
    ssh_object.connect_to_server_with_ssh()
    ssh_object.connect_to_channel()
    ssh_object.disable_modem_manager()
    ssh_object.enable_at_commands()
    ssh_object.get_modem_manufacturer_with_ssh()
    ssh_object.execute_at_commands_with_ssh()
    ssh_object.enable_modem_manager()
    ssh_object.close_ssh()
    return ssh_object.command_results


def get_command_results_with_serial(args, commands):
    serial_client = __import__('serial_client')
    serial_object = serial_client.SerialClient(
        args, commands)
    serial_object.connect_to_server_with_serial()
    serial_object.disable_modem_manager()
    serial_object.get_modem_manufacturer_with_serial()
    serial_object.execute_at_commands_with_serial()
    serial_object.enable_modem_manager()
    serial_object.close_serial()
    return serial_client.command_results


def get_at_command_results(args, commands):
    command_results = None
    match args['connection_type']:
        case 'ssh':
            command_results = get_command_results_with_ssh(args, commands)
        case 'serial':
            command_results = get_command_results_with_serial(args, commands)

        case _:
            print("Connection type must be 'serial' or 'ssh'")
            exit(1)
    return command_results


def print_command_results_to_csv(print_result_object):
    print_result_object.create_csv_filename()
    print_result_object.open_csv_file()
    print_result_object.write_to_csv_file()
    print_result_object.csv_file.close()


def upload_to_ftp_server(filename, ftp_server_data):
    ftp_upload = FTPUpload(filename, ftp_server_data)
    ftp_upload.open_ftp_session()
    ftp_upload.open_ftp_file()
    ftp_upload.store_ftp_file()
    ftp_upload.close_ftp()


def main():
    sys.path.append('src')
    args = get_arguments()
    device_name = args['d__device_name']
    enable_ftp = args['d__device_name']

    configuration_data = get_configuration_data(
        device_name, enable_ftp)
    command_results = get_at_command_results(args, configuration_data.commands)
    print_result_object = PrintResults(device_name, command_results)
    print_command_results_to_csv(print_result_object)
    if enable_ftp:
        upload_to_ftp_server(print_result_object.filename,
                             configuration_data.ftp_server_data)


if __name__ == '__main__':
    main()
