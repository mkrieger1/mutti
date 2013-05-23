import curses
from panel import Panel

class QuitScreen(Exception):
    pass

class Screen(Panel):
    def __init__(self, stdscr):
        Panel.__init__(self, win=stdscr)
        curses.curs_set(0)
        self.set_focus(True)

    def adopt(self, child):
        if not self.children:
            Panel.adopt(self, child)
        else:
            raise PanelError('can only have one child')

    def _update_size(self):
        c = self.children[0]
        return (c.min_height, c.min_width)

    def _layout(self, height, width):
        c = self.children[0]
        self.children[0].give_window()

    def _erase(self, height, width):
        self.win.erase()

    def _draw(self, height, width):
        pass

    def _handle_key(self, key):
        if key in map(ord, 'qQ'):
            raise QuitScreen
        else:
            return key

