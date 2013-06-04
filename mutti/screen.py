import curses
from panel import Panel
from status import Status
from colors import color_attr

class QuitScreen(Exception):
    pass

class Screen(Panel):
    _max_children = 2 # one of them is the statusbar

    def __init__(self, stdscr):
        Panel.__init__(self, win=stdscr)
        curses.curs_set(0)
        self.set_focus(True)
        statusbar = Status()
        self.adopt(statusbar)
        self.statusbar = statusbar

    def _get_size(self):
        min_height = sum(c.min_height for c in self.children)
        min_width  = sum(c.min_width  for c in self.children)
        max_height = sum(c.max_height for c in self.children)
        max_width  = sum(c.max_width  for c in self.children)
        return (min_height, min_width, max_height, max_width)

    def _layout(self, height, width):
        c = self.children[1]
        w = c.min_width
        h = min(c.min_height, height-1)
        top = max((height-h)/2, 0)
        left = max((width-w)/2, 0)
        c.give_window(height=h, width=w, top=top, left=left)
        self.statusbar.give_window(height=1, width=w, top=h+top, left=left)

    def _erase(self, height, width):
        self.win.erase()
        self.fill(height, width, '/~', color_attr("green"))

    def _draw(self, height, width):
        pass

    def _handle_key(self, key):
        if key in map(ord, 'qQ'):
            raise QuitScreen
        else:
            return key
