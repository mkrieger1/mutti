import curses


class PanelError(Exception):
    pass


class Panel:
    _focusable = True
    _allow_children = True

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

    def log(self, text):
        """
        Write text to log file (must be provided in advance).
        """
        try:
            print >> self._log, text
            self._log.flush()
        except:
            pass

    #--------------------------------------------------------------------

    def adopt(self, child):
        """
        Declare another panel as child.
        """
        if not self._allow_children:
            raise PanelError('children are not allowed')
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
        self.min_height, self.min_width = self._update_size()
        if self.parent:
            self.parent.update_size()

    def _update_size(self):
        """
        Calculate minimum size based on children.

        Must return a tuple (min_height, min_width).
        """
        raise NotImplementedError # needed if there are children

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
                raise PanelError(
                'failed to create subwindow %i %i at %i %i ' % (
                                   used_height, used_width, top, left) +
                '- parent window %i %i' % (self.parent.win.getmaxyx()))
            self._need_layout = True

    def take_window(self):
        """
        Remove the window to make panel invisible.
        """
        self.win = None

    #--------------------------------------------------------------------

    def handle_key(self, key):
        """
        Pass the key down to focused child, or do something with it.
        """
        # The top-level panel catches terminal resize events.
        if key == curses.KEY_RESIZE:
            self._need_layout = True
            return None
        # Normal keys are passed down to the focused child.
        # If we have no focused child or it didn't use the key (or it
        # generated a new key!), we handle it.
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
        if not self.win:
            return

        height, width = self.win.getmaxyx()
        if height == 0 or width == 0:
            return

        if self.children and self._need_layout:
            self._layout(height, width)
        self._need_layout = False

        self._erase(height, width)
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
        raise NotImplementedError # needed if there are children
            
    def _erase(self, height, width):
        """
        Erase the window, and draw the background.

        The children will be drawn on top.
        """
        pass # implement it in subclass, if needed
            
    def _draw(self, height, width):
        """
        Draw the foreground over the children.
        """
        pass # implement it in subclass, if needed

    #--------------------------------------------------------------------

    def set_focus(self, has_focus):
        if self._focusable:
            self.has_focus = has_focus
            if self.focused_child:
                self.focused_child.set_focus(has_focus)

    def _move_focus(self, amount):
        focus_children = [c for c in self.children if c._focusable]
        while True:
            self.focused_child_idx += amount
            if self.focused_child_idx not in range(len(focus_children)):
                self.focused_child_idx -= amount
                return False
            if self.focused_child:
                self.focused_child.set_focus(False)
            self.focused_child = focus_children[self.focused_child_idx]
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

