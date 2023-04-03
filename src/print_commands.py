import curses


class PrintCommands():

    def __init__(self, *args, **kwargs):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN,
                         curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED,
                         curses.COLOR_BLACK)

    def print_at_commands(self, device_name, command, expected_response, actual_response, passed, failed, total_commands):
        self.stdscr.addstr(0, 0, f"Testing product: {device_name}")
        self.stdscr.addstr(1, 0, f"Currently testing: {command}")
        self.stdscr.addstr(2, 0,
                           f"Expected response: {expected_response}")

        self.stdscr.addstr(3, 0, f"Actual response: {actual_response}")
        self.stdscr.addstr(
            4, 0, f"PASSED TESTS: {passed}", curses.color_pair(1))
        self.stdscr.addstr(
            5, 0, f"FAILED TESTS: {failed}", curses.color_pair(2))
        self.stdscr.addstr(6, 0, f"TOTAL TESTS: {total_commands}")
        self.stdscr.refresh()
        self.stdscr.erase()

    def del_curses(self):
        curses.echo()
        curses.nocbreak()
        curses.endwin()
