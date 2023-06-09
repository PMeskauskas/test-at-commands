import curses


class CommandPrinter():

    def __init__(self, *args, **kwargs):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN,
                         curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED,
                         curses.COLOR_BLACK)

    def print_at_commands(self, command_results):
        self.stdscr.addstr(
            0, 0, f"Testing product: {command_results['device_name']}, {command_results['model']}")
        self.stdscr.addstr(
            1, 0, f"Currently testing: {command_results['command']}")
        self.stdscr.addstr(2, 0,
                           f"Expected response: {command_results['expected_response']}")

        self.stdscr.addstr(
            3, 0, f"Actual response: {command_results['actual_response']}")
        self.stdscr.addstr(
            4, 0, f"PASSED TESTS: {command_results['passed_command_count']}", curses.color_pair(1))
        self.stdscr.addstr(
            5, 0, f"FAILED TESTS: {command_results['failed_command_count']}", curses.color_pair(2))
        self.stdscr.addstr(
            6, 0, f"TOTAL TESTS: {command_results['total_command_count']}")
        self.stdscr.refresh()
        self.stdscr.erase()

    def del_curses(self):
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def print_at_command_to_terminal(self, command_results):
        print(
            f"Tested product: {command_results['device_name']}, {command_results['model']}")
        print(f"Last command tested: {command_results['command']}")
        print(f"Expected response: {command_results['expected_response']}")

        print(f"Actual response: {command_results['actual_response']}")
        print(
            f"PASSED TESTS: {command_results['passed_command_count']}")
        print(
            f"FAILED TESTS: {command_results['failed_command_count']}")
        print(f"TOTAL TESTS: {command_results['total_command_count']}")
