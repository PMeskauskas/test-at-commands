from src.argument_parser import ArgumentParser
from src.results import Results
from src.ftp_upload import FTPUpload
from src.config_data import ConfigData
import sys


def check_connection_type(device):
    config_object = ConfigData(
        device['d__device_name'], device['enable_ftp'])
    match device['connection_type']:
        case 'ssh':
            ssh_client = __import__('ssh_client')
            ssh_object = ssh_client.SshClient(device, config_object.commands)

            result_object = Results(device['d__device_name'],
                                    ssh_object.command_results)
        case 'serial':
            serial_client = __import__('serial_client')
            serial_object = serial_client.SerialClient(
                device, config_object.commands)
            result_object = Results(device['d__device_name'],
                                    serial_object.command_results)

        case _:
            print("Connection type must be 'serial' or 'ssh'")
            exit(1)
    if device['enable_ftp']:
        FTPUpload(result_object.filename, config_object.ftp_server_data)


def main():
    sys.path.append('src')
    args = ArgumentParser()
    check_connection_type(args.arguments)


if __name__ == '__main__':
    main()
