import curses
import sys
import time

from screen import Screen, QuitScreen
from dial import Dial
from lists import PanelVList, PanelHList
from status import Status
from spacer import Spacer


def main(stdscr, *main_args):

    s = Status()
    mainscreen = Screen(stdscr)

    v = PanelVList() #stdscr, (4, 6))#, "random dials")
    for i in range(5):
        d = Dial(("Dial %02i"%i, 10), (2*i, 6), (-100, 100), s)
        v.adopt(d)
    v.adopt(s, align_ver='bottom')
    mainscreen.adopt(v)

    #d2 = PanelVList(stdscr, (4, 21))#, "random dials 2")
    #for i in range(7):
    #    d2.add_new(Dial, ("Dial2 %02i"%i, 9), (2*i, 4), (-100, 100))
    #h = PanelHList(stdscr, (3, 3))
    #h.add_existing(d)
    #h.add_existing(d2)

    while 1:
        #d.set_status(s)
        #d.redraw()
        #d2.redraw()
        mainscreen.redraw()
        curses.doupdate()
        key = stdscr.getch()
        try:
            mainscreen.handle_key(key)
        except QuitScreen:
            break
            

if __name__=='__main__':
    try:
        curses.wrapper(main, *sys.argv)
    except KeyboardInterrupt:
        pass

