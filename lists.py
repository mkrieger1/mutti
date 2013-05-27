import curses
import curses.ascii
from panel import Panel

class _PanelList(Panel):
    """
    Generic panel list (vertical or horizontal).
    """
    def __init__(self):
        Panel.__init__(self)
        self.align_hor = {}
        self.align_ver = {}

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
        self.align_hor[panel] = align_hor # has no meaning in HList
        self.align_ver[panel] = align_ver # has no meaning in VList

        

class PanelVList(_PanelList):
    """
    Vertical panel list.
    """
    _next_keys = [curses.ascii.TAB, curses.KEY_DOWN, ord('j')]
    _prev_keys = [curses.KEY_BTAB,  curses.KEY_UP,   ord('k')]

    def _get_size(self):
        min_height = sum(c.min_height for c in self.children)
        min_width = max(c.min_width for c in self.children)
        max_height = sum(c.max_height for c in self.children)
        max_width = max(c.max_width for c in self.children)
        return (min_height, min_width, max_height, max_width)

    def _layout(self, height, width): # TODO use focus
        top = 0
        for c in self.children:
            if top < height:
                c.give_window(top=top, height=c.min_height,
                              align_hor=self.align_hor[c])
                top += c.min_height
            else:
                c.take_window()
        

class PanelHList(_PanelList):
    """
    Horizontal panel list.
    """
    _next_keys = [curses.ascii.TAB, curses.KEY_RIGHT, ord('l')]
    _prev_keys = [curses.KEY_BTAB,  curses.KEY_LEFT, ord('h')]

    def _get_size(self):
        min_height = max(c.min_height for c in self.children)
        min_width = sum(c.min_width for c in self.children)
        max_height = max(c.max_height for c in self.children)
        max_width = sum(c.max_width for c in self.children)
        return (min_height, min_width, max_height, max_width)

    def _layout(self, height, width): # TODO use focus
        left = 0
        for c in self.children:
            if left < width:
                c.give_window(left=left, width=c.min_width,
                              align_ver=self.align_ver[c])
                left += c.min_width
            else:
                c.take_window()

