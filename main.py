import curses
import sys
import time

from dial import Dial, DialList
from status import Status


def main(stdscr, *main_args):
    curses.curs_set(0)

    stdscr.box()
    d = DialList(stdscr, (4, 6))
    for i in range(5):
        d.add_dial(("Dial %02i"%i, 8), (2*i, 4), (-100, 100))
    s = Status(stdscr, (stdscr.getmaxyx()[0]-1, 0))

    while 1:
        d.set_status(s)
        d.redraw()
        s.redraw()
        curses.doupdate()
        key = stdscr.getch()
        if key == ord('q'):
            break
        else:
            d.handle_key(key)
            

if __name__=='__main__':
    main_args = sys.argv
    try:
        curses.wrapper(main, *main_args)
    except KeyboardInterrupt:
        pass

