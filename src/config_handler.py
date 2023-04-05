import json


class ConfigHandler:
    def __init__(self, config_file_name):
        self.config_file_name = config_file_name
        self.config_file = None
        self.data = None
        self.commands = None
        self.ftp_server_data = None

    def open_configuration_file(self):
        try:
            self.config_file = open(self.config_file_name, 'r')
        except FileNotFoundError:
            print(f"Configuration file '{self.config_file_name}' not found")
            exit(1)

    def load_configuration_data(self):
        try:
            self.data = json.load(self.config_file)
        except json.JSONDecodeError:
            print('Failed to load JSON configuration data')
            exit(1)

    def get_commands_by_device_name(self, device_name):
        try:
            self.commands = self.data['device'][0][device_name]
        except KeyError:
            print(
                f"No configured commands found for device: {device_name}")
            available_devices = [
                device for device in self.data['device'][0].keys()]
            available_devices = ' '.join(available_devices)
            print(f"Available device configurations: {available_devices}")
            exit(1)

    def get_ftp_server_data(self):
        try:
            self.ftp_server_data = self.data['ftp_server']
            self.check_if_ftp_server_arguments_exists()
        except KeyError:
            print(
                f"No FTP server configuration data found")
            exit(1)

    def check_if_ftp_server_arguments_exists(self):
        if not "hostname" in self.ftp_server_data:
            exit("Missing 'hostname' argument in configuration file")

        if not "username" in self.ftp_server_data:
            exit("Missing 'username' argument in configuration file")

        if not "password" in self.ftp_server_data:
            exit("Missing 'password' argument in configuration file")

    def parse_device_configuration_data(self):

        for i in range(0, len(self.commands)):
            self.check_if_command_arguments_exists(self.commands[i])

            arguments = self.commands[i]['argument']
            command = self.commands[i]['command']
            arguments = arguments.split(',')
            parsed_argument = f"{command}="
            for argument in arguments:
                argument = argument.replace('"', '')
                if argument != "":
                    if argument.isnumeric() or argument == "?":
                        parsed_argument += f"{argument},"
                    else:
                        parsed_argument += f"\"{argument}\","
            parsed_argument = parsed_argument[:-1]
            self.commands[i]["command"] = parsed_argument
        exit(1)

    def check_if_command_arguments_exists(self, command):
        if not "command" in command:
            exit("Missing 'command' argument in configuration file")

        if not "argument" in command:
            exit("Missing 'argument' argument in configuration file")

        if not "expected" in command:
            exit("Missing 'expected' argument in configuration file")

    def close_configuration_file(self):
        try:
            self.config_file.close()
        except:
            exit(f"Failed to close configuration file")
