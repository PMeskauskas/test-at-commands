def parse_arguments():
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
    return args
