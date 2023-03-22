class PrintCommands():

    def __init__(self):
        self.curses = __import__('curses')
        self.stdscr = self.curses.initscr()
        self.curses.noecho()
        self.curses.cbreak()
        self.curses.start_color()
        self.curses.init_pair(1, self.curses.COLOR_GREEN,
                              self.curses.COLOR_BLACK)
        self.curses.init_pair(2, self.curses.COLOR_RED,
                              self.curses.COLOR_BLACK)

    def print_at_commands(self, device_name, command, expected_response, actual_response, passed, failed, total_commands):
        self.stdscr.addstr(0, 0, f"Testing product: {device_name}")
        self.stdscr.addstr(1, 0, f"Currently testing: {command}")
        self.stdscr.addstr(2, 0,
                           f"Expected response: {expected_response}")

        self.stdscr.addstr(3, 0, f"Actual response: {actual_response}")
        self.stdscr.addstr(
            4, 0, f"PASSED TESTS: {passed}", self.curses.color_pair(1))
        self.stdscr.addstr(
            5, 0, f"FAILED TESTS: {failed}", self.curses.color_pair(2))
        self.stdscr.addstr(6, 0, f"TOTAL TESTS: {total_commands}")
        self.stdscr.refresh()
        self.stdscr.erase()

    def del_curses(self):
        self.curses.echo()
        self.curses.nocbreak()
        self.curses.endwin()
