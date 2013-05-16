import curses

class Panel:
    def __init__(self, parent, top, left, height, width):
        self.parent = parent
        self.win = None

        self.top = top
        self.left = left
        self.height = height
        self.width = width

            
    def draw(self, height, width):
        raise NotImplementedError


    def redraw(self):
        max_height, max_width = self.parent.getmaxyx()
        vis_height = min(self.height, max(max_height - self.top,  0))
        vis_width  = min(self.width,  max(max_width  - self.left, 0))
        #  
        #        A vis_height
        #        |
        # height + . . . . . . ,------
        #        |            / .     
        #        |           /  .     
        #        |          /   .     
        #        |         /    .     
        #        |        /     .     
        #      0 +-------´      .     
        #        L-------+------+-----------> max_height
        #                top    top+height

        if vis_height == 0 or vis_width == 0:
            self.win = None
            return

        if self.win is None:
            recreate = True
        else: # self.win exists
            sub_height, sub_width = self.win.getmaxyx()
            sub_top,    sub_left  = self.win.getparyx()

            recreate = any(sub_height != vis_height,
                           sub_width  != vis_width,
                           sub_top    != self.top,
                           sub_left   != self.left)
        if recreate:
            self.win = self.parent.subwin(vis_height, vis_width,
                                          self.top, self.left)
        self.win.erase()
        self.draw(vis_height, vis_width)
        self.win.refresh()

                            

