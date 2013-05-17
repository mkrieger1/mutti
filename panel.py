import curses

class Panel:
    def __init__(self, parent, pos=None, size=None):
        self.parent = parent
        p_height, p_width = parent.getmaxyx()

        if pos is None:
            self.top = 0
            self.left = 0
        else:
            self.top, self.left = pos

        if size is None:
            self.height = p_height - self.top
            self.width  = p_width - self.left
        else:
            self.height, self.width = size

        self.win = None


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
            self.win = None
            return

        if self.win is None:
            self.win = self.parent.subwin(vis_height, vis_width,
                                          self.top, self.left)
        else:
            # subwindow shrinks automatically, but does not grow
            sub_height, sub_width = self.win.getmaxyx()
            grow = any([sub_height < vis_height,
                        sub_width  < vis_width,
                       ])
            if grow:
                self.win.resize(vis_height, vis_width)

            #sub_top, sub_left = self.win.getparyx()
            #moved = any([sub_top  != self.top, # ?
            #             sub_left != self.left # ?
            #            ])

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

