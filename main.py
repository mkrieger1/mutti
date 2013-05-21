import curses
import sys
import time

from dial import Dial
from lists import PanelVList, PanelHList
from status import Status


def main(stdscr, *main_args):
    curses.curs_set(0)

    stdscr.box()
    d = PanelVList(stdscr, (4, 6))#, "random dials")
    for i in range(5):
        d.add_new(Dial, ("Dial %02i"%i, 8), (2*i, 4), (-100, 100))
    d2 = PanelVList(stdscr, (4, 21))#, "random dials 2")
    for i in range(7):
        d2.add_new(Dial, ("Dial2 %02i"%i, 9), (2*i, 4), (-100, 100))
    h = PanelHList(stdscr, (3, 3))
    h.add_existing(d)
    h.add_existing(d2)
    s = Status(stdscr, (stdscr.getmaxyx()[0]-1, 0))

    while 1:
        #d.set_status(s)
        #d.redraw()
        #d2.redraw()
        h.redraw()
        s.redraw()
        curses.doupdate()
        key = stdscr.getch()
        if key == ord('q'):
            break
        else:
            h.handle_key(key)
            

if __name__=='__main__':
    main_args = sys.argv
    try:
        curses.wrapper(main, *main_args)
    except KeyboardInterrupt:
        pass

