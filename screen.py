import curses
from panel import Panel, PanelError

class Screen(Panel):
    def __init__(self, stdscr):
        Panel.__init__(self, win=stdscr)
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

