import curses
import sys
import time

from screen import Screen, QuitScreen
from dial import Dial
from lists import PanelVList, PanelHList
from status import Status
from align import VAlign, HAlign
from toggle import Toggle


def main(stdscr, *main_args):
    curses.use_default_colors()
    f = open('loglog.log', 'w')
    mainscreen = Screen(stdscr)

    statusbar = Status(width=80)
    statusbar._log = f
    status_bottom = VAlign(align='bottom', height=30)
    status_bottom.adopt(statusbar)

    hlisttop = PanelHList()

    vlist = PanelVList()
    vlist._log = f
    for i in range(5):
        d = Dial("Dial %02i"%i, (-100, 100), 6, 2*i)
        d._status = statusbar
        d._log = f
        vlist.adopt(d)
    vlist.adopt(status_bottom)

    hlist = PanelHList()
    hlist._log = f
    for i in range(3):
        d = Dial("Dial %02i"%i, (-100, 100), 6, 2*i)
        d._status = statusbar
        hlist.adopt(d)
    hlist_bottom = VAlign(align='center', height=20)
    hlist_bottom.adopt(hlist)
    vlist.adopt(hlist_bottom)

    vlist2 = PanelVList()
    vlist2._log = f
    for i in range(5):
        t = Toggle("Toggle %02i"%i)
        t._status = statusbar
        t._log = f
        vlist2.adopt(t)
    for i in range(5):
        t = Toggle("ToToToggle %02i"%i)
        t._status = statusbar
        t._log = f
        vlist2.adopt(t)
    for i in range(5):
        t = Toggle("InvisibleToggle %02i"%i, draw_label=False)
        t._status = statusbar
        t._log = f
        vlist2.adopt(t)

    hlisttop.adopt(vlist)
    hlisttop.adopt(vlist2)

    mainscreen.adopt(hlisttop)
    mainscreen._log = f


    while 1:
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

