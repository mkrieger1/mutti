import curses


class PanelError(Exception):
    pass


class Panel:
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
        self.focused_child = None
        self.has_focus = False


    def adopt(self, child):
        """
        Declare a panel as child.
        """
        self.children.append(child)
        child.parent = self
        self._need_layout = True


    def give_window(self, child, height=None, width=None,
                                 top=None, left=None,
                                 align_ver='top', align_hor='left'):
        """
        Create a subwindow for a child.

        height, width, top, and left specify the area in the parent window
        that is allowed to be used, if they are not given, the maximum
        available space is used (if needed).
        """
        if top is None:
            top = 0
        if left is None:
            left = 0
        if height is None:
            height = self.win.getmaxyx()[0]-top
        if width is None:
            width = self.win.getmaxyx()[1]-left

        if height < child.min_height:
            #raise PanelError('need at least %i columns' % child.min_height)
            # deal with it!
            pass
        if width < child.min_width:
            #raise PanelError('need at least %i rows' % child.min_width)
            # deal with it!
            pass

        if child.max_height is not None:
            height = min(height, child.max_height)
            remaining_height = height - child.max_height
            top += {'top':    0,
                    'center': remaining_height/2,
                    'bottom': remaining_height
                   }[align_ver]
        if child.max_width is not None:
            width = min(width, child.max_width)
            remaining_width = width - child.max_width
            left += {'left':   0,
                     'center': remaining_width/2,
                     'right':  remaining_width
                    }[align_hor]

        child.win = self.win.derwin(height, width, top, left)
        child._need_layout = True



    def handle_key(self, key):
        if key == curses.KEY_RESIZE:
            self._need_layout = True
            return
        if self.focused_child:
            key = self.focused_child.handle_key(key)
        if key is not None:
            return self._handle_key(key)

    def _handle_key(self, key):
        """
        Do something depending on the key, or return the key.

        """
        raise NotImplementedError



    def redraw(self):
        """
        Redraw the panel and all children.
        """
        height, width = self.win.getmaxyx()
        if height == 0 or width == 0:
            return

        if self._need_layout:
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
        window is too small.
        """
        raise NotImplementedError
            
    def _draw(self, height, width):
        """
        Given the window size, draw the panel.
        """
        raise NotImplementedError



                            
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

