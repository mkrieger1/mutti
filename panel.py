import curses

class Panel:
    def __init__(self, min_height=None, min_width=None,
                       max_height=None, max_width=None, win=None):
        """Specify minimum/maximum size and optionally set the window.
        
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


    def adopt(self, child, height=None, width=None, top=None, left=None):
        """Declare a panel as child and create a subwindow for it.

        height, width, top, and left specify the area in the parent window
        that is allowed to be used, if they are not given, the maximum
        available space is used (if needed).
        """

        self.children.append(child)
        child.parent = self

        if top is None:
            top = 0
        if left is None:
            left = 0
        if height is None:
            height = self.win.getmaxyx()[0]-top
        if width is None:
            width = self.win.getmaxyx()[1]-left

        if height < child.min_height:
            raise ValueError('need at least %i columns' % child.min_height)
        if width < child.min_width:
            raise ValueError('need at least %i rows' % child.min_width)

        if child.max_height is not None:
            height = min(height, child.max_height)
        if child.max_width is not None:
            width = min(width, child.max_width)

        child.win = self.win.derwin(height, width, top, left)


    def handle_key(self, key):
        raise NotImplementedError

            
    def draw(self):
        raise NotImplementedError


    def redraw(self):
        max_height, max_width = self.parent.getmaxyx()
        vis_height = min(self.height, max(max_height - self.top,  0))
        vis_width  = min(self.width,  max(max_width  - self.left, 0))
        #  
        #        A vis_height
        #        |
        # height + . . . . . . *******
        #        |            *.     
        #        |           * .     
        #        |          *  .     
        #        |         *   .     
        #        |        *    .     
        #      0 +********     .     
        #        L-------+-----+-----------> max_height
        #                top   top+height

        if vis_height == 0 or vis_width == 0:
            return

        else:
            # subwindow shrinks automatically, but does not grow
            sub_height, sub_width = self.win.getmaxyx()
            grow = any([sub_height < vis_height,
                        sub_width  < vis_width,
                       ])
            if grow:
                self.win.resize(vis_height, vis_width)

        self.win.erase()
        self.draw()
        self.win.noutrefresh()


    def hline(self, y, x, length, attr=curses.A_NORMAL):
        if self.win:
            try:
                self.win.hline(y, x, curses.ACS_HLINE|attr, length)
            except curses.error:
                pass


    def vline(self, y, x, length, attr=curses.A_NORMAL):
        if self.win:
            try:
                self.win.vline(y, x, curses.ACS_VLINE|attr, length)
            except curses.error:
                pass

                            
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

