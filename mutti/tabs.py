import curses
import curses.ascii
from panel import Panel
from util import distribute_space, shorten_label
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
        self._last_distr = None

    def adopt(self, panel, label):
        Panel.adopt(self, panel)
        self._labels.append("%i: %s" % (len(self._labels)+1, label))

    #--------------------------------------------------------------------

    def _handle_key(self, key):
        if key in map(ord, '123456789'):
            i = int(chr(key))-1
        elif key in map(ord, 'tW'):
            i = (self.focus_idx + 1) % len(self.children)
        elif key in map(ord, 'TB'):
            i = (self.focus_idx - 1) % len(self.children)
        else:
            return key
        if i in range(len(self.children)):
            if i == self.focus_idx:
                return None
            elif not self._move_focus_to(i):
                return key
            else:
                self._need_layout = True

    #--------------------------------------------------------------------

    def _get_size(self):
        min_height = max(c.min_height for c in self.children) + 2
        min_width  = max(c.min_width  for c in self.children)
        max_height = None
        max_width  = None
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
        """
        Draw the foreground (tab labels and lines).
        """
        # step 1: distribute the available width
        fi = self.focus_idx
        if (not self._last_distr or
         self._last_distr[0] != width or
         self._last_distr[1][fi] != len(self._labels[fi])+3):
            # for each label: " label |"
            give = [len(label)+3 for label in self._labels]
            distribute_space(width, fi, give)
            self._last_distr = (width, give)
        else:
            give = self._last_distr[1]

        # step 2: draw labels and lines
        for x in range(width):
            self.addch(1, x, curses.ACS_HLINE)
        left = 0
        for (i, label) in enumerate(self._labels):
            w = give[i] # given width
            L = w-3     # available for the label
            b = len(label) # needed for the label
            if w > 0:
                if i == fi:
                    attr = curses.A_BOLD
                    self.addch(1, left-1, curses.ACS_LRCORNER)
                    self.addstr(1, left, ' '*w)
                else:
                    attr = curses.A_NORMAL
                if L < b:
                    labelstr = shorten_label(label, L)
                else:
                    labelstr = label
                    self.addch(0, left+w-1, curses.ACS_VLINE)
                    self.addch(1, left+w-1, curses.ACS_LLCORNER if i == fi
                                       else curses.ACS_BTEE)
                self.addstr(0, left+1, labelstr, attr)
            left += w
        if give[0] < len(self._labels[0])+3:
            self.addch(1, 0, curses.ACS_LARROW)
        if give[-1] < len(self._labels[-1])+3:
            self.addch(1, width-1, curses.ACS_RARROW)

