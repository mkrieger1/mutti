import curses
from panel import Panel

class Screen(Panel):
    def __init__(self, stdscr):
        Panel.__init__(self, win=stdscr)
        self.set_focus(True)

    def _update_size(self):
        pass

    def _layout(self, height, width):
        self.children[0].give_window(height=height-2, width=width-2,
                                     top=1, left=1)

    def _draw(self, height, width):
        self.win.box()

