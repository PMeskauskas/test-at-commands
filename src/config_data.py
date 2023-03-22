def open_configuration_file(config_file_name):
    try:
        config_file = open(config_file_name, 'r')
    except FileNotFoundError:
        print(f"Configuration file '{config_file_name}' not found")
        exit(1)
    return config_file


def load_configuration_data(config_file):
    try:
        json = __import__("json")
        data = json.load(config_file)
    except json.JSONDecodeError:
        print('Failed to load JSON configuration data')
        exit(1)
    return data


def get_commands_by_device_name(data, device_name):
    try:
        commands = data['device'][0][device_name]
    except KeyError:
        print(
            f"No configured commands found for device: {device_name}")
        available_devices = [device for device in data['device'][0].keys()]
        available_devices = ' '.join(available_devices)
        print(f"Available device configurations: {available_devices}")
        exit(1)
    return commands


def check_if_arguments_exists(command):
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


def parse_configuration_data(data, device_name):
    commands = get_commands_by_device_name(data, device_name)
    for i in range(0, len(commands)):
        arguments_exists = check_if_arguments_exists(commands[i])

        if not arguments_exists:
            exit(1)

        argument = commands[i]['argument']
        command = commands[i]['command']

        if argument != "":
            if argument.isnumeric() or argument == "?":
                commands[i]["command"] = f"{command}={argument}"
            else:
                commands[i]["command"] = f"{command}=\"{argument}\""
    return commands


def get_at_commands(device_name):
    config_file = open_configuration_file('config.json')
    data = load_configuration_data(config_file)
    commands = parse_configuration_data(data, device_name)
    config_file.close()
    return commands
