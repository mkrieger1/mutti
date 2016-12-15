import curses
from .panel import Panel

class Status(Panel):
    """A widget to display one line of text."""

    _focusable = False
    _max_children = 0

    def __init__(self, width=None):
        Panel.__init__(self, min_height=1, max_height=1, min_width=width)
        self._draw_task = None

    def _erase(self, height, width):
        if not self._draw_task:
            self.win.erase()

    def _draw(self, height, width):
        self.win.bkgd(' ', curses.A_REVERSE)
        try:
            self._draw_task(self)
        except:
            pass

