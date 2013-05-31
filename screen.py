import curses
from panel import Panel
from colors import color_attr

class QuitScreen(Exception):
    pass

class Screen(Panel):
    _max_children = 1

    def __init__(self, stdscr):
        Panel.__init__(self, win=stdscr)
        curses.curs_set(0)
        self.set_focus(True)

    def _get_size(self):
        c = self.children[0]
        return c._get_size()

    def _layout(self, height, width):
        c = self.children[0]
        w = c.min_width
        h = c.min_height
        top = max((height-h)/2, 0)
        left = max((width-w)/2, 0)
        self.children[0].give_window(height=h, width=w, top=top, left=left)

    def _erase(self, height, width):
        self.win.erase()
        self.fill(height, width, '/ ', color_attr("green"))

    def _draw(self, height, width):
        pass

    def _handle_key(self, key):
        if key in map(ord, 'qQ'):
            raise QuitScreen
        else:
            return key

