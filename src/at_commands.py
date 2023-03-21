
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


def print_at_commands(stdscr, curses, device_name, command, expected_response, actual_response, passed, failed, total_commands):
    stdscr.addstr(0, 0, f"Testing product: {device_name}")
    stdscr.addstr(1, 0, f"Currently testing: {command}")
    stdscr.addstr(2, 0,
                  f"Expected response: {expected_response}")

    stdscr.addstr(3, 0, f"Actual response: {actual_response}")
    stdscr.addstr(
        4, 0, f"PASSED TESTS: {passed}", curses.color_pair(1))
    stdscr.addstr(5, 0, f"FAILED TESTS: {failed}", curses.color_pair(2))
    stdscr.addstr(6, 0, f"TOTAL TESTS: {total_commands}")
    stdscr.refresh()
    stdscr.erase()


def init_stdscr(curses):
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    return stdscr


def del_curses(curses):
    curses.echo()
    curses.nocbreak()
    curses.endwin()
