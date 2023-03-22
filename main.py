
def check_connection_type(device):
    results = __import__("results")
    match device['connection_type']:
        case 'ssh':
            ssh_client = __import__('ssh_client')
            command_results = ssh_client.test_at_commands_with_ssh(device)
            results.form_csv(device, command_results)
        case 'serial':
            serial_client = __import__('serial_client')
            command_results = serial_client.test_at_commands_with_serial(
                device)
            results.form_csv(device, command_results)
        case _:
            print("Connection type must be 'serial' or 'ssh'")


def main():
    sys = __import__('sys')
    sys.path.append('src')
    argument_parser = __import__("argument_parser")
    args = argument_parser.parse_arguments()
    check_connection_type(vars(args))


if __name__ == '__main__':
    main()
