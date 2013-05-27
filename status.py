import curses
from panel import Panel

class Status(Panel):
    """A widget to display one line of text."""

    _focusable = False

    def __init__(self):
        Panel.__init__(self, min_height=1, max_height=1, max_width=80)
        self.text = ''

    def set(self, text):
        self.text = text

    def _erase(self, height, width):
        self.win.erase()

    def _draw(self, height, width):
        self.win.bkgd(' ', curses.A_REVERSE)
        self.addstr(0, 0, self.text)

