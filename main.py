import curses
import sys
import time

import panel

class LinePanel(panel.Panel):
    def draw(self, height, width):
        self.win.box()
        (y, x) = self.win.getmaxyx()
        self.addstr(1, 1, str(y))
        self.addstr(2, 1, str(x))
        self.hline(self.height-2, 0, self.width)

class MainPanel(panel.Panel):
    def draw(self, height, width):
        (y, x) = self.win.getmaxyx()
        self.addstr(1, 1, str(y))
        self.addstr(2, 1, str(x))

def main(stdscr, *main_args):
    curses.curs_set(0)
    p = MainPanel(stdscr)
    q = LinePanel(stdscr, 10, 10, 40, 50)
    r = LinePanel(stdscr,  7, 13, 40, 50)
    while 1:
        p.redraw()
        q.redraw()
        r.redraw()
        key = stdscr.getch()

if __name__=='__main__':
    main_args = sys.argv
    try:
        curses.wrapper(main, *main_args)
    except KeyboardInterrupt:
        pass

