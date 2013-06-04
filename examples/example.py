import curses

from mutti.screen import Screen, QuitScreen
from mutti.status import Status
from mutti.tabs import Tabs
from mutti.lists import VList, HList
from mutti.align import VAlign
from mutti.grid import Grid
from mutti.dial import Dial
from mutti.toggle import Toggle

#--------------------------------------------------------------------

def build_panels(stdscr):
    mainscreen = Screen(stdscr)
    # The status bar, which various panels will draw on, belongs to the
    # main screen, so that it is in the foreground.
    statusbar = mainscreen.statusbar

    # first tab: vertical list with dials and nested, vertically centered,
    # horizontal list with more dials
    vlist = VList()
    for i in range(5):
        d = Dial("Dial %02i"%i, (-100, 100), 6, 2*i)
        d._status = statusbar
        vlist.adopt(d)

    hlist = HList()
    for i in range(3):
        d = Dial("Dial %02i"%i, (-100, 100), 6, 2*i)
        d._status = statusbar
        hlist.adopt(d)
    d = Dial("Another Dial", (-100, 100), 6, 10)
    hlist.adopt(d)
    hlist_align = VAlign(align='center', height=20)
    hlist_align.adopt(hlist)
    vlist.adopt(hlist_align)

    # second tab: vertical list with toggles, some with invisible labels
    vlist2 = VList()
    for i in range(10):
        t = Toggle("Toggle %02i"%i)
        t._status = statusbar
        vlist2.adopt(t)
    for i in range(5):
        t = Toggle("InvisibleToggle %02i"%i, draw_label=False)
        t._status = statusbar
        vlist2.adopt(t)
    for i in range(10):
        t = Toggle("AnotherToggle %02i"%i)
        t._status = statusbar
        vlist2.adopt(t)

    # third tab: grid with toggles and dials
    rows, cols = 10, 10
    g = Grid(rows, cols)
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

    tabs = Tabs()
    tabs.adopt(vlist, "First VList")
    tabs.adopt(vlist2, "Second VList")
    tabs.adopt(g, "Grid")

    mainscreen.adopt(tabs)

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

def main(stdscr):
    curses.use_default_colors()
    top_panel = build_panels(stdscr)
    main_loop(top_panel)

if __name__=='__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass

