

def check_connection_type(device):
    results = __import__("results")

    match device['connection_type']:
        case 'ssh':
            ssh_client = __import__('ssh_client')
            ssh_object = ssh_client.SshClient(device)

            results.Results(device['d__device_name'],
                            ssh_object.command_results)
        case 'serial':
            serial_client = __import__('serial_client')
            serial_object = serial_client.SerialClient(device)
            results.Results(device['d__device_name'],
                            serial_object.command_results)
        case _:
            print("Connection type must be 'serial' or 'ssh'")


def main():
    sys = __import__('sys')
    sys.path.append('src')
    argument_parser = __import__("argument_parser")
    args = argument_parser.ArgumentParser()
    check_connection_type(args.arguments)


if __name__ == '__main__':
    main()
