import curses
from panel import Panel

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
        self.children[0].give_window(
            align_ver='center', align_hor='center')

    def _erase(self, height, width):
        self.win.erase()

    def _draw(self, height, width):
        pass

    def _handle_key(self, key):
        if key in map(ord, 'qQ'):
            raise QuitScreen
        else:
            return key

