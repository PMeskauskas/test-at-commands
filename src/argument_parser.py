import argparse


class ArgumentParser:
    def __init__(self, *args, **kwargs):
        self.arguments = None

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
        parser.add_argument("--enable_ftp", action="store",
                            help="Option to upload to FTP server (True,False)", const=1, nargs="?", default="false")

        self.arguments = parser.parse_args()
        self.arguments = vars(self.arguments)

    def adjust_case_sensitivity(self):
        self.arguments['d__device_name'] = self.arguments['d__device_name'].upper()
        self.arguments['connection_type'] = self.arguments['connection_type'].lower()

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

    def check_upload_to_ftp(self):
        upload_ftp_argument = self.arguments['enable_ftp'].lower()
        if upload_ftp_argument == 'true':
            self.arguments['enable_ftp'] = True
        elif upload_ftp_argument == 'false':
            self.arguments['enable_ftp'] = False
        else:
            print("Upload to FTP argument should be true or false")
            exit(1)
