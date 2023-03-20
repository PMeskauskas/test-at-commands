import logging


def get_at_commands(device_name):
    with open('config.json', 'r') as config_file:
        json = __import__("json")
        data = json.load(config_file)
        try:
            commands = data['device'][0][device_name]
            logging.info(f"Got AT commands for {device_name}")
            return commands
        except KeyError:
            logging.error(
                f"No configured commands found for device: {device_name}")
            available_devices = [device for device in data['device'][0].keys()]
            available_devices = ' '.join(available_devices)
            logging.error(f"Available devices: {available_devices}")
            exit(1)
