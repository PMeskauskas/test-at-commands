def get_at_commands(device_name):
    with open('config.json', 'r') as config_file:
        json = __import__("json")
        data = json.load(config_file)
        try:
            commands = data['device'][0][device_name]

            for i in range(0, len(commands)):
                argument = commands[i]['argument']
                command = commands[i]['command']
                if argument != "":
                    if argument.isnumeric() or argument == "?":
                        commands[i]["command"] = f"{command}={argument}"
                    else:
                        commands[i]["command"] = f"{command}=\"{argument}\""
            return commands
        except KeyError:
            print(
                f"No configured commands found for device: {device_name}")
            available_devices = [device for device in data['device'][0].keys()]
            available_devices = ' '.join(available_devices)
            print(f"Available devices: {available_devices}")
            exit(1)
