import curses

INF = float('inf')

class PanelError(Exception):
    pass

class ExitLoop(Exception):
    pass


class Panel:
    _focusable = True
    _max_children = INF

    def __init__(self, min_height=None, min_width=None,
                       max_height=None, max_width=None):
        """
        Specify minimum/maximum size and optionally set the window.

        Minimum size means the size that the panel will need to be drawn
        completely.
        Maximum size means the size that the panel will occupy if the
        available drawing area is infinite.
        
        If minimum/maximum size are not given, they default to (0, 0) and
        (inf, inf), respectively.
        """
        self.min_height = min_height or 0
        self.min_width  = min_width  or 0
        self.max_height = max_height or INF
        self.max_width  = max_width  or INF

        self.win = None
        self.parent = None
        self.children = []
        self.focus_idx = 0
        self.focused_child = None

        self.has_focus = False

    #--------------------------------------------------------------------

    def run(self):
        """
        Run the application with this panel as top panel.
        """
        # workaround for strange behaviour in interactive mode
        # see http://bugs.python.org/issue2675
        if not __name__=='__main__':
            import os
            for v in ['LINES', 'COLUMNS']:
                os.unsetenv(v)
        def main(stdscr):
            curses.use_default_colors()
            curses.curs_set(0)
            self.win = stdscr
            while 1:
                self.redraw()
                curses.doupdate()
                key = self.win.getch()
                try:
                    self.handle_key(key)
                except ExitLoop:
                    break
        curses.wrapper(main)

    #--------------------------------------------------------------------

    def log(self, *text):
        """
        Write text to log file (must be provided in advance).
        """
        try:
            print >> self._log, str(self), " ".join(map(str, text))
            self._log.flush()
        except:
            pass

    #--------------------------------------------------------------------

    def adopt(self, child, update_size=True):
        """
        Declare another panel as child.
        """
        if len(self.children) >= self._max_children:
            raise PanelError('additional children are not allowed')
        self.children.append(child)
        # If there are many children, update_size can be skipped to save
        # time. It must then be called explicitly after all children are
        # adopted.
        if update_size:
            self.update_size()
        child.parent = self
        if not self.focused_child:
            if child._focusable:
                self.focused_child = child
                self.focus_idx = len(self.children)-1
                self.set_focus(self.has_focus)
        self._need_layout = True

    def update_size(self):
        """
        Set the current minimum/maximum size and tell the parent to do so.

        A panel should do this whenever it changed its state in a way
        that influences its minimum or maximum size, for example if a
        child is adopted.
        """
        (min_height, min_width,
         max_height, max_width) = self._get_size()

        self.min_height = min_height or 0
        self.min_width  = min_width  or 0
        self.max_height = max_height or INF
        self.max_width  = max_width  or INF

        if self.parent:
            self.parent.update_size()

    def _get_size(self):
        """
        Calculate minimum and maximum size of a panel.

        Must return a tuple (min_height, min_width,
                             max_height, max_width).
        None as minimum value will be converted to 0.
        None as maximum value will be converted to INF.
        """
        if self._max_children:
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
        top  = top  or 0
        left = left or 0

        height = height or INF
        width  = width  or INF

        av_height = min(height, self.parent.win.getmaxyx()[0]-top)
        av_width  = min(width,  self.parent.win.getmaxyx()[1]-left)

        used_height = min(av_height, self.max_height)
        used_width  = min(av_width,  self.max_width)

        remaining_height = av_height - used_height
        remaining_width  = av_width  - used_width

        top += {'top'   : 0,
                'center': remaining_height/2,
                'bottom': remaining_height
               }[align_ver]

        left += {'left'  : 0,
                 'center': remaining_width/2,
                 'right' : remaining_width
                }[align_hor]

        try:
            self.win = self.parent.win.derwin(used_height, used_width,
                                              top, left)
        except curses.error:
            raise PanelError(
            '%s failed to create subwindow %i %i at %i %i ' % (
                str(self), used_height, used_width, top, left) +
            '- parent window %i %i' % (self.parent.win.getmaxyx()))

        self._layout(used_height, used_width)
        self._need_layout = False

    def take_window(self):
        """
        Remove the window to make panel invisible.
        """
        for c in self.children:
            c.take_window()
        self._need_layout = False
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
            if 1:#key is not None:
                return self._handle_key(key)
                # TODO test if this is a problem anywhere

    def _handle_key(self, key):
        """
        Do something depending on the key, or return the key.

        The key is not None.
        """
        if self._focusable:
            raise NotImplementedError # needed if has focus

    #--------------------------------------------------------------------

    def redraw(self):
        """
        Redraw the panel and all children.
        """
        if not self.win:
            return

        height, width = self.win.getmaxyx()
        if height == 0 or width == 0:
            self.take_window()
            return

        if self.children and self._need_layout:
            self._layout(height, width)
            self._need_layout = False

        self._erase(height, width)
        for child in self.children:
            child.redraw()
        self._draw(height, width)

        if self.has_focus:
            self._draw_status()

        self.win.noutrefresh()

    def _layout(self, height, width):
        """
        Given the window size, create subwindows for the children.

        This should also handle which children are visible, in case the
        window is too small. Use c.give_window() for each visible child c.
        """
        if self._max_children:
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

    def _draw_status(self):
        try:
            self._status._draw_task = self._get_status_draw_task()
            self._status.redraw()
        except:
            pass

    def _get_status_draw_task(self):
        """
        Create a function which draws onto the status bar.

        The status bar must be the only parameter of the function.
        """
        return None # implement it in subclass, if needed

    #--------------------------------------------------------------------

    def set_focus(self, has_focus):
        success = False
        if self._focusable:
            self.has_focus = has_focus
            success = True
        if self.focused_child:
            success |= self.focused_child.set_focus(has_focus)
        return success

    def _move_focus_to(self, i):
        """
        Move the focus to the i-th child.

        Returns True if successful, or False if there is no focusable
        i-th child.
        """
        if self.children[i].set_focus(True):
            self.focused_child.set_focus(False)
            self.focused_child = self.children[i]
            self.focus_idx = i
            fc = self.focused_child
            if (not fc.win or
                fc.win.getmaxyx()[0] < fc.min_height or
                fc.win.getmaxyx()[1] < fc.min_width):
                self._need_layout = True
            return True
        else:
            return False

    def _move_focus(self, direction):
        """
        Move the focus to next or previous child.

        Returns True if successful, or False if there is no focusable
        next or previous child.
        """
        amount = 1 if direction > 0 else -1
        i = self.focus_idx + amount

        while True:
            if i not in range(len(self.children)):
                return False
            elif self._move_focus_to(i):
                return True
            else:
                i += amount

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

    def fill(self, height, width, string, attr=curses.A_NORMAL, top=0, left=0):
        y = top
        x = left
        while y < height:
            x = x % (width-left)
            while x < width:
                self.addstr(y, x, string, attr)
                x += len(string)
            y += 1

