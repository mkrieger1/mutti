import curses
import sys
import time

def initkey(win):
    win.addstr(2,  2, "key",  curses.A_BOLD)
    win.addstr(2, 12, "code", curses.A_STANDOUT)
    win.box()

def showkey(win, key):
    oldbkgd = win.getbkgd()
    win.move(3, 2)
    win.clrtoeol()
    win.bkgdset(ord(' '), curses.A_NORMAL)
    try:
        win.addstr(3, 2, chr(key), curses.A_NORMAL)
    except ValueError:
        pass
    win.addstr(3, 12, str(key), curses.A_NORMAL)
    win.bkgdset(oldbkgd)
    win.refresh()

def main(stdscr, *main_args):
    curses.curs_set(0)
    s1 = stdscr.subwin(10, 10, 20, 13)
    s2 = stdscr.subwin(14, 25, 18, 15)
    s1.bkgd(ord(' '), curses.A_REVERSE)
    s2.bkgd(ord(' '), curses.A_REVERSE)
    initkey(stdscr)
    s1.addstr(0, 0, "hallo1")
    s2.addstr(0, 0, "hallo2")

    while True:
        key = stdscr.getch()
        showkey(stdscr, key)

if __name__=='__main__':
    main_args = sys.argv
    try:
        curses.wrapper(main, *main_args)
    except KeyboardInterrupt:
        pass

