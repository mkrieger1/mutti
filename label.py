import curses
from panel import Panel
from util import shorten_label


class Label(Panel):
    """
    Panel to display one line of text.
    """
    _focusable = False
    _max_children = 0

    def __init__(self, text):
        w = len(text)
        Panel.__init__(self, min_width=w, max_width=w,
                             min_height=1, max_height=1)
        self.text = text

    def _handle_key(self, key):
        return key

    def _erase(self, height, width):
        self.win.erase()
            
    def _draw(self, height, width):
        text = shorten_label(self.text, width)
        self.addstr(0, 0, text)

