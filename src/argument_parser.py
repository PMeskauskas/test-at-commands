import argparse


class ArgumentParser:
    def __init__(self):

        self.arguments = None
        self.parse_arguments()
        self.adjust_case_sensitivity()
        self.check_connectivity()

    def parse_arguments(self):

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
        self.arguments = parser.parse_args()
        self.arguments = vars(self.arguments)

    def adjust_case_sensitivity(self):
        device_name_upper = self.arguments['d__device_name'].upper()
        connection_type_lower = self.arguments['connection_type'].lower()
        self.arguments['d__device_name'] = device_name_upper
        self.arguments['connection_type'] = connection_type_lower

    def check_connectivity(self):
        device_name = self.arguments['d__device_name']
        connection_type = self.arguments['connection_type']
        if connection_type == 'ssh':
            if 'TRM' in device_name:
                print(
                    f"{connection_type} connection is not possible with {device_name} device")
                exit(1)
        if connection_type == 'serial':
            if 'TRM' not in device_name:
                print(
                    f"{connection_type} connection is not possible with {device_name} device")
                exit(1)
