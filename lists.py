import curses
from panel import Panel

class _PanelList(Panel):
    """Generic panel list (vertical or horizontal)."""

    def __init__(self, parent, pos):
        Panel.__init__(self, parent, pos, (0, 0))
        self.panels = []
        self.focus = 0
        self.is_focused = True

    def add_existing(self, panel):
        self._calc_geom(panel)
        self.panels.append(panel)
        if self.is_focused:
            self.panels[self.focus]._focus()

    def add_new(self, panelclass, *args):
        pos = self._new_pos()
        p = panelclass(self.win, pos, *args)
        self.add_existing(p)

    def _calc_geom(self, newpanel):
        raise NotImplementedError

    def _new_pos(self):
        raise NotImplementedError

    def _focus(self):
        self.panels[self.focus]._focus()
        Panel._focus(self)

    def _defocus(self):
        self.panels[self.focus]._defocus()
        Panel._defocus(self)

    def set_focus(self, i):
        self.panels[self.focus]._defocus()
        self.focus = i % len(self.panels)
        if self.is_focused:
            self.panels[self.focus]._focus()

    def focus_next(self):
        self.set_focus(self.focus + 1)

    def focus_prev(self):
        self.set_focus(self.focus - 1)

    def draw(self):
        for p in self.panels:
            p.redraw()

    def handle_key(self, key):
        if key is None:
            return
        elif key in map(ord, map(str, range(1, len(self.panels)+1))):
            self.set_focus(int(chr(key))-1)
        elif key in self._next_keys:
            self.focus_next()
        elif key in self._prev_keys:
            self.focus_prev()
        else:
            return self.panels[self.focus].handle_key(key)
        

class PanelVList(_PanelList):
    """Vertical panel list."""

    _next_keys = [curses.KEY_DOWN, ord('j')]
    _prev_keys = [curses.KEY_UP, ord('k')]

    def _new_pos(self):
        return self.height, 0

    def _calc_geom(self, newpanel):
        self.height += newpanel.height
        self.width = max(self.width, newpanel.width)
        

class PanelHList(_PanelList):
    """Horizontal panel list."""

    _next_keys = [curses.KEY_RIGHT, ord('l')]
    _prev_keys = [curses.KEY_LEFT, ord('h')]

    def _new_pos(self):
        return 0, self.width

    def _calc_geom(self, newpanel):
        self.height = max(self.height, newpanel.height)
        self.width += newpanel.width

