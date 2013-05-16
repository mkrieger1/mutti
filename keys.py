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

