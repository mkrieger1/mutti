import curses


class PanelError(Exception):
    pass


class Panel:
    _focusable = True

    def __init__(self, min_height=None, min_width=None,
                       max_height=None, max_width=None, win=None):
        """
        Specify minimum/maximum size and optionally set the window.
        
        If minimum/maximum size are not given, they default to (0, 0) and
        the available size in the window, respectively.
        """
        if min_height is None:
            min_height = 0
        if min_width is None:
            min_width = 0
        self.min_height = min_height
        self.min_width = min_width
        self.max_height = max_height
        self.max_width = max_width

        self.win = win

        self.parent = None
        self.children = []
        self.focused_child_idx = 0
        self.focused_child = None

        self.has_focus = False

    #--------------------------------------------------------------------

    def adopt(self, child):
        """
        Declare another panel as child.
        """
        self.children.append(child)
        child.parent = self
        self.update_size()
        if not self.focused_child:
            if child._focusable:
                self.focused_child = child
                self.focused_child_idx = len(self.children)-1
                self.set_focus(self.has_focus)
        self._need_layout = True

    def update_size(self):
        self._update_size()
        if self.parent:
            self.parent.update_size()

    def _update_size(self):
        """
        Calculate minimum size based on children.
        """
        raise NotImplementedError

    #--------------------------------------------------------------------

    def give_window(self, height=None, width=None, top=None, left=None,
                          align_ver='top', align_hor='left'):
        """
        Create a subwindow for a child (self being the child).

        height, width, top, and left specify the area in the parent window
        that is allowed to be used, if they are not given, the maximum
        available space is used (if needed).
        """
        if top is None:
            top = 0
        if left is None:
            left = 0
        if height is None:
            height = self.parent.win.getmaxyx()[0]-top
        if width is None:
            width = self.parent.win.getmaxyx()[1]-left

        if self.max_height is not None:
            used_height = min(height, self.max_height)
        else:
            used_height = height
        remaining_height = height - used_height
        top += {'top':    0,
                'center': remaining_height/2,
                'bottom': remaining_height
               }[align_ver]

        if self.max_width is not None:
            used_width = min(width, self.max_width)
        else:
            used_width = width
        remaining_width = width - used_width
        left += {'left':   0,
                 'center': remaining_width/2,
                 'right':  remaining_width
                }[align_hor]

        if (not self.win or (used_height, used_width) != self.win.getmaxyx() or
                                          (top, left) != self.win.getbegyx()):
            try:
                self.win = self.parent.win.derwin(used_height, used_width, top, left)
            except curses.error:
                raise RuntimeError(' '.join(map(str,
                                   [used_height, used_width, top, left])))
            self._need_layout = True

    #--------------------------------------------------------------------

    def handle_key(self, key):
        if key == curses.KEY_RESIZE:
            self._need_layout = True
        else:
            if self.focused_child:
                key = self.focused_child.handle_key(key)
            if key is not None:
                return self._handle_key(key)

    def _handle_key(self, key):
        """
        Do something depending on the key, or return the key.

        The key is not None.
        """
        raise NotImplementedError

    #--------------------------------------------------------------------

    def redraw(self):
        """
        Redraw the panel and all children.
        """
        height, width = self.win.getmaxyx()
        if height == 0 or width == 0:
            return

        if self.children and self._need_layout:
            self._layout(height, width)
        self._need_layout = False

        self.win.erase()
        for child in self.children:
            child.redraw()
        self._draw(height, width)
        self.win.noutrefresh()

    def _layout(self, height, width):
        """
        Given the window size, create subwindows for the children.

        This should also handle which children are visible, in case the
        window is too small. Use c.give_window() for each visible child c.
        """
        raise NotImplementedError
            
    def _draw(self, height, width):
        """
        Given the window size, draw the panel.

        The children have already been drawn
        """
        raise NotImplementedError

    #--------------------------------------------------------------------

    def set_focus(self, has_focus):
        if self._focusable:
            self.has_focus = has_focus
            if self.focused_child:
                self.focused_child.set_focus(has_focus)

    def _move_focus(self, amount):
        while True:
            self.focused_child_idx += amount
            if self.focused_child_idx not in range(len(self.children)):
                self.focused_child_idx -= amount
                return False
            if self.children[self.focused_child_idx]._focusable:
                if self.focused_child:
                    self.focused_child.set_focus(False)
                self.focused_child = self.children[self.focused_child_idx]
                self.focused_child.set_focus(True)
                return True
        # TODO _need_layout

    def focus_next(self):
        return self._move_focus(1)

    def focus_prev(self):
        return self._move_focus(-1)

    #--------------------------------------------------------------------
                            
    def addch(self, y, x, char, attr=curses.A_NORMAL):
        if self.win:
            try:
                self.win.addch(y, x, char, attr)
            except curses.error:
                pass
                            
    def addstr(self, y, x, string, attr=curses.A_NORMAL):
        if self.win:
            try:
                self.win.addstr(y, x, string, attr)
            except curses.error:
                pass

