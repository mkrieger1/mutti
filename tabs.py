import curses
import curses.ascii
from panel import Panel
from lists import _layout_distr
from colors import color_attr


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
            i = int(chr(key))-1
            if i in range(len(self.children)):
                if i == self.focus_idx:
                    return None
                elif not self._move_focus_to(i):
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
            self.focused_child.give_window(h, w, top=2,
                                           align_hor='center',
                                           align_ver='center')
        else:
            self.focused_child.take_window()


    def _erase(self, height, width):
        self.win.erase()


    def _draw(self, height, width):
        for x in range(width):
            self.addch(1, x, curses.ACS_HLINE)
        left = 0
        give = [len(label)+3 for label in self._labels]
        # one space left, one space and one line right
        want = [0 for label in self._labels]
        _layout_distr(self.focus_idx, width, give, want)
        for (i, label) in enumerate(self._labels):
            L = give[i]
            if L > 0:
                self.addch(0, left+L-1, curses.ACS_VLINE)
                self.addch(1, left+L-1, curses.ACS_BTEE)
                if i == self.focus_idx:
                    attr = curses.A_BOLD
                    self.addch(1, left-1, curses.ACS_LRCORNER)
                    self.addstr(1, left, ' '*L)
                    self.addch(1, left+L-1, curses.ACS_LLCORNER)
                else:
                    attr = curses.A_NORMAL
                labelstr = label[:L-3]+'~' if L < len(label) else label
                self.addstr(0, left+1, labelstr, attr)
            left += L

