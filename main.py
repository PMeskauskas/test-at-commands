from src.argument_parser import ArgumentParser
from src.results import Results
import sys


def check_connection_type(device):

    match device['connection_type']:
        case 'ssh':
            ssh_client = __import__('ssh_client')
            ssh_object = ssh_client.SshClient(device)

            Results(device['d__device_name'],
                    ssh_object.command_results)
        case 'serial':
            serial_client = __import__('serial_client')
            serial_object = serial_client.SerialClient(device)
            Results(device['d__device_name'],
                    serial_object.command_results)
        case _:
            print("Connection type must be 'serial' or 'ssh'")


def main():
    sys.path.append('src')
    args = ArgumentParser()
    check_connection_type(args.arguments)


if __name__ == '__main__':
    main()
