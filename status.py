import curses
from panel import Panel

class Status(Panel):
    """A widget to display one line of text."""

    def __init__(self):
        Panel.__init__(self, min_height=1)
        self.text = ''
        self._focusable = False

    def set(self, text):
        self.text = text

    def _draw(self, height, width):
        self.win.bkgd(' ', curses.A_REVERSE)
        self.addstr(0, 0, self.text)

