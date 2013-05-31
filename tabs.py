import curses
import curses.ascii
from panel import Panel
from lists import _layout_distr


class Tabs(Panel):
    """
    Arrange panels in tabs.
    """

    _max_children = 9 # in principle there can be more, but then you have
                      # to think of a better way for navigating than using
                      # the 1-9 keys...

    def __init__(self, *args):
        Panel.__init__(self, *args)
        self._labels = []

    def adopt(self, panel, label):
        Panel.adopt(self, panel)
        self._labels.append(label)

    #--------------------------------------------------------------------

    def _handle_key(self, key):
        if key in map(ord, '123456789'):
            self.log("handling %i (%s)" % (key, chr(key)))
            i = int(chr(key))-1
            self.log("i = %i" % i)
            if i in range(len(self.children)):
                if not self._move_focus_to(i):
                    return key
                else:
                    self._need_layout = True
        else:
            return key

    #--------------------------------------------------------------------

    def _get_size(self):
        min_height = max(c.min_height for c in self.children) + 2
        min_width  = max(c.min_width  for c in self.children)
        max_height = max(c.max_height for c in self.children) + 2
        max_width  = max(c.max_width  for c in self.children)
        return (min_height, min_width, max_height, max_width)


    def _layout(self, height, width):
        for c in self.children:
            c.take_window()
        h = height-2
        w = width
        if h > 0 and w > 0:
            self.focused_child.give_window(h, w, top=2)
        else:
            self.focused_child.take_window()


    def _erase(self, height, width):
        self.win.erase()


    def _draw(self, height, width):
        for x in range(width):
            self.addch(1, x, curses.ACS_HLINE)
        left = 0
        for (i, label) in enumerate(self._labels):
            attr = curses.A_BOLD if i == self.focus_idx else 0
            self.addstr(0, left, label, attr)
            left += len(label)+1

