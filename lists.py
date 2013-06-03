import curses
import curses.ascii
from panel import Panel

#--------------------------------------------------------------------

def _layout_distr(focus_idx, available, give, want=None):
    """
    Distribute available space to children, priority to focused.

    Result list "give" is modified in-place.
    """
    if not want:
        want = [0 for g in give]
    # not even enough space for focused child
    if available < give[focus_idx]:
        for i in range(len(give)):
            give[i] = 0 if i != focus_idx else available
    # not enough space for every child -> trim
    elif available < sum(give):
        over = sum(give) - available
        i = 0
        j = len(give)-1
        while True:
            if j > focus_idx:
                if give[j] >= over:
                    give[j] -= over
                    break
                else:
                    over -= give[j]
                    give[j] = 0
                    j -= 1
            if i < focus_idx:
                if give[i] >= over:
                    if focus_idx <= j < len(give)-1:
                        j += 1
                        give[j] += give[i]
                        over += give[i]
                over -= give[i]
                give[i] = 0
                i += 1
                if over <= 0:
                    break
    # enough space for every child -> give more to those who want
    else:
        i = 0
        while sum(give) < available and sum(want) > 0:
            if want[i] > 0:
                want[i] -= 1
                give[i] += 1
            i = (i+1)%len(give)

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
        _layout_distr(self.focus_idx, height, give, want)

        arrows = [0, 0]
        for i in [0, -1]:
            if give[i] < self.children[i].min_height:
                arrows[i] = 1

        w = max(c.min_width for c in self.children)
        top = 0
        for (c, h) in zip(self.children, give):
            if h > 0:
                uparrow = top == 0 and arrows[0]
                dnarrow = h+top == height and arrows[1]
                wi = w-1 if uparrow or dnarrow else w
                if uparrow:
                    wi -= 1
                if dnarrow:
                    wi -= 1
                if height > 1:
                    wi = max(wi, w-2)
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
        _layout_distr(self.focus_idx, width, give, want)

        h = max(c.min_height for c in self.children)
        left = 0
        for (c, w) in zip(self.children, give):
            if w > 0:
                c.give_window(left=left, height=h, width=w,
                              align_ver=self._align_ver[c])
                left += w
            else:
                c.take_window()

