import curses
from .panel import Panel


class Frame(Panel):
    """
    Display a panel inside a frame.
    """
    _max_children = 1

    def __init__(self, label, *args):
        Panel.__init__(self, *args)
        self.label = label

    def _handle_key(self, key):
        return key

    def _get_size(self):
        min_height = max(c.min_height for c in self.children) + 2
        min_width  = max(c.min_width  for c in self.children) + 2
        max_height = max(c.max_height for c in self.children) + 2
        max_width  = max(c.max_width  for c in self.children) + 2
        return (min_height, min_width, max_height, max_width)

    def _layout(self, height, width):
        h = height-2
        w = width-2
        c = self.children[0]
        if h > 0 and w > 0:
            c.give_window(h, w, top=1, left=1,
                          align_hor='center', align_ver='center')
        else:
            c.take_window()

    def _erase(self, height, width):
        self.win.erase()
            
    def _draw(self, height, width):
        self.win.box()
        attr = curses.A_BOLD if self.has_focus else curses.A_NORMAL
        self.addstr(0, 1, self.label, attr)

