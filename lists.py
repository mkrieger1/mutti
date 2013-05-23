import curses
from panel import Panel

class _PanelList(Panel):
    """Generic panel list (vertical or horizontal)."""

    def __init__(self):
        Panel.__init__(self)
        self.align_hor = {}
        self.align_ver = {}

    def _draw(self, height, width):
        pass

    def _handle_key(self, key):
        #if key in map(ord, map(str, range(1, len(self.children)+1))):
        #    self.set_focus(int(chr(key))-1)
        if key in self._next_keys:
            self.focus_next()
        elif key in self._prev_keys:
            self.focus_prev()
        else:
            return key

    def add(self, panel, align_hor='left', align_ver='top'):
        self.adopt(panel)
        self.align_hor[panel] = align_hor
        self.align_ver[panel] = align_ver

        

class PanelVList(_PanelList):
    """Vertical panel list."""

    _next_keys = [curses.KEY_DOWN, ord('j')]
    _prev_keys = [curses.KEY_UP, ord('k')]

    def _update_size(self):
        self.min_height = sum(c.min_height for c in self.children)
        self.min_width = max(c.min_width for c in self.children)

    def _layout(self, height, width):
        if height >= self.min_height:
            top = 0
            for c in self.children:
                c.give_window(height=None, top=top,
                              align_hor=self.align_hor[c],
                              align_ver=self.align_ver[c])
                top += c.min_height
        else: # TODO use focus
            top = 0
            for c in self.children:
                if top+c.min_height > height:
                    c.take_window()
                else:
                    c.give_window(height=None, top=top)
                    top += c.min_height
        

class PanelHList(_PanelList):
    """Horizontal panel list."""

    _next_keys = [curses.KEY_RIGHT, ord('l')]
    _prev_keys = [curses.KEY_LEFT, ord('h')]

    def _update_size(self, newpanel):
        self.height = max(self.height, newpanel.height)
        self.width += newpanel.width

    def _layout(self, height, width):
        if width >= self.min_width:
            left = 0
            for c in self.children:
                c.give_window(width=c.min_width, left=left,
                              align_hor=self.align_hor[c],
                              align_ver=self.align_ver[c])
                left += c.min_width
        else: # TODO use focus
            left = 0
            for c in self.children:
                c.give_window(width=c.min_width, left=left)
                left += c.min_width
                if left >= self.min_width:
                    break

