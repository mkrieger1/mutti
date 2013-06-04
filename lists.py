import curses
import curses.ascii
from panel import Panel
from util import distribute_space

#--------------------------------------------------------------------

class _PanelList(Panel):
    """
    Generic panel list (vertical or horizontal).
    """
    def __init__(self):
        Panel.__init__(self)
        self._align_hor = {}
        self._align_ver = {}

    def _erase(self, height, width):
        self.win.erase()

    def _draw(self, height, width):
        pass

    def _handle_key(self, key):
        #if key in map(ord, map(str, range(1, len(self.children)+1))):
        #    self.set_focus(int(chr(key))-1)
        if key in self._next_keys:
            if not self.focus_next():
                return key
        elif key in self._prev_keys:
            if not self.focus_prev():
                return key
        else:
            return key

    def adopt(self, panel, align_hor='left', align_ver='top'):
        Panel.adopt(self, panel)
        self._align_hor[panel] = align_hor # has no meaning in HList
        self._align_ver[panel] = align_ver # has no meaning in VList

#--------------------------------------------------------------------

class PanelVList(_PanelList):
    """
    Vertical panel list.
    """
    _next_keys = [curses.ascii.TAB, curses.KEY_DOWN, ord('j'), ord('w')]
    _prev_keys = [curses.KEY_BTAB,  curses.KEY_UP,   ord('k'), ord('b')]

    def _get_size(self):
        if not self.children:
            return
        min_height = sum(c.min_height for c in self.children)
        min_width = max(c.min_width for c in self.children)
        max_height = sum(c.max_height for c in self.children)
        max_width = max(c.max_width for c in self.children)
        return (min_height, min_width, max_height, max_width)

    def _layout(self, height, width):
        if not self.children:
            return
        give = [c.min_height for c in self.children]
        want = [c.max_height-c.min_height for c in self.children]
        distribute_space(height, self.focus_idx, give, want)

        arrows = [give[i] < self.children[i].min_height
                  for i in [0, -1]]

        w = max(c.min_width for c in self.children)
        top = 0
        for (c, h) in zip(self.children, give):
            if h > 0:
                uparrow = 1 if   top == 0      and arrows[0] else 0
                dnarrow = 1 if h+top == height and arrows[1] else 0
                wi = {0: w,
                      1: w-2,
                      2: w-2 if height > 1 else w-3
                     }[uparrow+dnarrow]
                c.give_window(top=top, height=h, width=wi,
                              align_hor=self._align_hor[c])
                top += h
            else:
                c.take_window()

    def _draw(self, height, width):
        if not self.children:
            return
        c = self.children[0]
        uparrow = not c.win or c.win.getmaxyx()[0] < c.min_height
        c = self.children[-1]
        dnarrow = not c.win or c.win.getmaxyx()[0] < c.min_height

        if uparrow:
            xup = width-1 if height > 1 or not dnarrow else width-2
            self.addch(0, xup, curses.ACS_UARROW)
        if dnarrow:
            xdn = width-1
            self.addch(height-1, xdn, curses.ACS_DARROW)


class PanelHList(_PanelList):
    """
    Horizontal panel list.
    """
    _next_keys = [curses.ascii.TAB, curses.KEY_RIGHT, ord('l'), ord('w')]
    _prev_keys = [curses.KEY_BTAB,  curses.KEY_LEFT,  ord('h'), ord('b')]

    def _get_size(self):
        if not self.children:
            return
        min_height = max(c.min_height for c in self.children)
        min_width = sum(c.min_width for c in self.children)
        max_height = max(c.max_height for c in self.children)
        max_width = sum(c.max_width for c in self.children)
        return (min_height, min_width, max_height, max_width)

    def _layout(self, height, width):
        if not self.children:
            return
        give = [c.min_width for c in self.children]
        want = [c.max_width-c.min_width for c in self.children]
        distribute_space(width, self.focus_idx, give, want)

        arrows = [give[i] < self.children[i].min_width
                  for i in [0, -1]]
        if any(arrows):
            distribute_space(width-sum(arrows), self.focus_idx, give)
        left = 1 if arrows[0] else 0

        h = max(c.min_height for c in self.children)
        for (c, w) in zip(self.children, give):
            if w > 0:
                c.give_window(left=left, height=h, width=w,
                              align_ver=self._align_ver[c])
                left += w
            else:
                c.take_window()

    def _draw(self, height, width):
        if not self.children:
            return
        c = self.children[0]
        larrow = not c.win or c.win.getmaxyx()[1] < c.min_width
        c = self.children[-1]
        rarrow = not c.win or c.win.getmaxyx()[1] < c.min_width

        if larrow:
            self.addch(0, 0, curses.ACS_LARROW)
        if rarrow:
            self.addch(0, width-1, curses.ACS_RARROW)

