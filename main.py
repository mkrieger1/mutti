import curses
import sys
import time

from screen import Screen, QuitScreen
from dial import Dial
from lists import PanelVList, PanelHList
from status import Status
from align import VAlign, HAlign
from toggle import Toggle
from grid import Grid
from tabs import Tabs

#--------------------------------------------------------------------

def build_panels(stdscr):
    f = open('loglog.log', 'w')
    mainscreen = Screen(stdscr)
    mainscreen._log = f

    statusbar = mainscreen.statusbar
    statusbar._log = f

    tabs = Tabs()

    vlist = PanelVList()
    #vlist._log = f
    for i in range(5):
        d = Dial("Dial %02i"%i, (-100, 100), 6, 2*i)
        d._status = statusbar
        #d._log = f
        vlist.adopt(d)

    hlist = PanelHList()
    #hlist._log = f
    for i in range(3):
        d = Dial("Dial %02i"%i, (-100, 100), 6, 2*i)
        d._status = statusbar
        hlist.adopt(d)
    hlist_align = VAlign(align='center', height=20)
    hlist_align.adopt(hlist)
    vlist.adopt(hlist_align)

    vlist2 = PanelVList()
    #vlist2._log = f
    for i in range(5):
        t = Toggle("Toggle %02i"%i)
        t._status = statusbar
        #t._log = f
        vlist2.adopt(t)
    for i in range(5):
        t = Toggle("ToToToggle %02i"%i)
        t._status = statusbar
        #t._log = f
        vlist2.adopt(t)
    for i in range(5):
        t = Toggle("InvisibleToggle %02i"%i, draw_label=False)
        t._status = statusbar
        #t._log = f
        vlist2.adopt(t)

    rows, cols = 10, 10
    g = Grid(rows, cols)
    #g._log = f
    for row in range(rows):
        for col in range(cols):
            if not row == col:
                t = Toggle("Tog%i%i" % (row, col), draw_label=True)
                t._status = statusbar
                g.adopt(t, row, col)
            else:
                d = Dial("Dial%i%i" % (row, col), (-32, 32), 3)
                d._status = statusbar
                g.adopt(d, row, col)

    tabs.adopt(vlist, "first VList")
    tabs.adopt(vlist2, "second VList")
    tabs.adopt(g, "Grid")
    for i in range(6):
        tabs.adopt(PanelVList(),  "dummy list %i" % i)
    tabs._log = f
    
    vlist_main = PanelVList()
    vlist_main.adopt(tabs)

    mainscreen.adopt(vlist_main)

    return mainscreen

#--------------------------------------------------------------------

def main_loop(top_panel):
    """
    Run the application.

    top_panel must be a Panel instance with top_panel.win == stdscr.
    """
    while 1:
        top_panel.redraw()
        curses.doupdate()
        key = top_panel.win.getch()
        try:
            top_panel.handle_key(key)
        except QuitScreen:
            break

def main(stdscr, *main_args):
    curses.use_default_colors()
    top_panel = build_panels(stdscr)
    main_loop(top_panel)

if __name__=='__main__':
    try:
        curses.wrapper(main, *sys.argv)
    except KeyboardInterrupt:
        pass

