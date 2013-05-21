import curses
from panel import Panel

class Status(Panel):
    """A widget to display one line of text."""

    def __init__(self, parent, pos):
        _, p_width = parent.getmaxyx()
        Panel.__init__(self, parent, pos, (1, p_width))
        self.text = ''

    def set(self, text):
        self.text = text

    def draw(self):
        self.win.bkgd(' ', curses.A_REVERSE)
        self.addstr(0, 0, self.text)

