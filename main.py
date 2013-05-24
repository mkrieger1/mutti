import curses
import sys
import time

from screen import Screen, QuitScreen
from dial import Dial
from lists import PanelVList, PanelHList
from status import Status
from align import VAlign


def main(stdscr, *main_args):
    mainscreen = Screen(stdscr)

    statusbar = Status()
    status_bottom = VAlign(align_ver='bottom')
    status_bottom.adopt(statusbar)

    vlist = PanelVList()
    for i in range(5):
        d = Dial(("Dial %02i"%i, 10), (2*i, 6), (-100, 100), statusbar)
        vlist.adopt(d)
    vlist.adopt(status_bottom)
    mainscreen.adopt(vlist)

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

