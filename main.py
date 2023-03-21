
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
    argparse = __import__('argparse')
    parser = argparse.ArgumentParser(description="Program to automatically test AT commands",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d" "--device-name", required=True, action="store",
                        help="Device name (for example: RUTX11, TRM240)")
    parser.add_argument("-c", "--connection-type", required=True,
                        action="store", help="Connection type (ssh, serial)")
    parser.add_argument("-p", "--serial-port",
                        action="store", help="Serial usb port", default='/dev/ttyUSB2')
    parser.add_argument("--ip-address", action="store",
                        help="Server IP address", const=1, nargs="?", default="192.168.1.1")
    parser.add_argument("-u", "--username", action="store",
                        help="Server username", const=1, nargs="?", default="root")
    parser.add_argument("-P", "--password", action="store",
                        help="Server password", const=1, nargs="?", default="Admin123")
    args = parser.parse_args()
    check_connection_type(vars(args))


if __name__ == '__main__':
    main()
