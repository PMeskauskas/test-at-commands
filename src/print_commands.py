def init_stdscr(curses):
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    return stdscr


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


def del_curses(curses):
    curses.echo()
    curses.nocbreak()
    curses.endwin()
