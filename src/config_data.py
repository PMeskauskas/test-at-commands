class ConfigData:
    def __init__(self, device_name):
        self.device_name = device_name
        self.config_file_name = 'config.json'
        self.config_file = None
        self.data = None
        self.commands = None

        self.open_configuration_file()
        self.load_configuration_data()
        self.get_commands_by_device_name()
        self.parse_configuration_data()

        self.config_file.close()

    def open_configuration_file(self):
        try:
            self.config_file = open(self.config_file_name, 'r')
        except FileNotFoundError:
            print(f"Configuration file '{self.config_file_name}' not found")
            exit(1)

    def load_configuration_data(self):
        try:
            json = __import__("json")
            self.data = json.load(self.config_file)
        except json.JSONDecodeError:
            print('Failed to load JSON configuration data')
            exit(1)

    def get_commands_by_device_name(self):
        try:
            self.commands = self.data['device'][0][self.device_name]
        except KeyError:
            print(
                f"No configured commands found for device: {self.device_name}")
            available_devices = [
                device for device in self.data['device'][0].keys()]
            available_devices = ' '.join(available_devices)
            print(f"Available device configurations: {available_devices}")
            exit(1)

    def parse_configuration_data(self):

        for i in range(0, len(self.commands)):
            arguments_exists = self.check_if_arguments_exists(self.commands[i])

            if not arguments_exists:
                exit(1)

            argument = self.commands[i]['argument']
            command = self.commands[i]['command']

            if argument != "":
                if argument.isnumeric() or argument == "?":
                    self.commands[i]["command"] = f"{command}={argument}"
                else:
                    self.commands[i]["command"] = f"{command}=\"{argument}\""

    def check_if_arguments_exists(self, command):
        if not "command" in command:
            print("Missing 'command' argument in configuration file")
            return False
        if not "argument" in command:
            print("Missing 'argument' argument in configuration file")
            return False
        if not "expected" in command:
            print("Missing 'expected' argument in configuration file")
            return False
        return True
