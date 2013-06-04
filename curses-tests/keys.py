"""
Program for showing the numeric code and the names within the curses and
the curses.ascii modules of pressed keys.
"""
import curses
import curses.ascii

def initkey(win):
    win.addstr(2,  2, "key",  curses.A_BOLD)
    win.addstr(2, 12, "code", curses.A_BOLD)
    win.addstr(2, 22, "curses name", curses.A_BOLD)
    win.addstr(2, 42, "curses.ascii name", curses.A_BOLD)
    win.box()

def showkey(win, key):
    win.move(3, 2)
    win.clrtoeol()

    # key
    try:
        win.addstr(3, 2, chr(key))
    except ValueError:
        pass

    # code
    win.addstr(3, 12, str(key))

    # curses name
    name = [name for name in curses.__dict__ if name.startswith("KEY_") and
                                                key == curses.__dict__[name]]
    if name:
        win.addstr(3, 22, name[0])

    # curses.ascii name
    name = [name for name in curses.ascii.__dict__
            if name.startswith("") and key == curses.ascii.__dict__[name]]
    if name:
        win.addstr(3, 42, name[0])

    win.refresh()


def main(stdscr):
    curses.curs_set(0)
    initkey(stdscr)
    while 1:
        key = stdscr.getch()
        showkey(stdscr, key)


if __name__=='__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass

