import curses
from panel import Panel

class Status(Panel):
    """A widget to display one line of text."""

    _focusable = False
    _max_children = 0

    def __init__(self, width=None):
        Panel.__init__(self, min_height=1, max_height=1, max_width=width)

    def _erase(self, height, width):
        pass

    def _draw(self, height, width):
        self.win.bkgd(' ', curses.A_REVERSE)
        try:
            self._draw_task(self)
        except:
            pass

