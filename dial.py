import curses
import curses.textpad
import curses.ascii
from panel import Panel

class AbortEdit(Exception):
    pass

class Dial(Panel):
    """A widget to display and manipulate one numeric value."""

    _max_children = 0

    def __init__(self, label, vrange, digits,
                       value=None, min_width=None, max_width=None):
        self.vmin, self.vmax = vrange
        self.digits = digits+1
        min_width = min_width or len(label)+self.digits+1
        min_width = max(min_width, self.digits)
        max_width = max_width or min_width
        Panel.__init__(self, min_height=1, min_width=min_width,
                             max_height=1, max_width=max_width)
        self.step = 10
        if value is None:
            if self.vmin <= 0 <= self.vmax:
                value = 0
            else:
                value = self.vmin
        self.set(value)

        self.label = label
        #self.statuspanel = statuspanel


    #--------------------------------------------------------------------
    # Panel method overrides
    #--------------------------------------------------------------------
    def _handle_key(self, key):
        if key in [ord('+'), ord('a')-96]: # -96 = CTRL
            self.inc(1)
        elif key in [ord('-'), ord('x')-96]:
            self.dec(1)
        elif key in [curses.KEY_PPAGE, ord('u')-96]:
            self.inc(self.step)
        elif key in [curses.KEY_NPAGE, ord('d')-96]:
            self.dec(self.step)
        elif key == ord('s'):
            if self.text_input():
                return curses.ascii.TAB # focus next
        else:
            return key

    def _erase(self, height, width):
        self.win.erase()

    def _draw(self, height, width):
        attr = curses.A_BOLD if self.has_focus else curses.A_NORMAL

        labelstr = self.label
        if len(labelstr) > width-self.digits:
            labelstr = labelstr[:width-self.digits-1]+'~'

        self.addstr(0, 0,
                    labelstr, attr)
        self.addstr(0, width-self.digits,
                    str(self.value).rjust(self.digits-1), attr)


    #--------------------------------------------------------------------
    # custom methods
    #--------------------------------------------------------------------
    def set(self, value):
        if value > self.vmax:
            self.value = self.vmax
        elif value < self.vmin:
            self.value = self.vmin
        else:
            self.value = value

    def inc(self, amount):
        self.set(self.value+amount)

    def dec(self, amount):
        self.set(self.value-amount)

    #def set_status(self):
    #    bar_len = 20
    #    bar_pos = ((self.value - self.vmin) * bar_len / 
    #               (self.vmax  - self.vmin))
    #    bar = '#'*bar_pos + '-'*(bar_len-bar_pos)
    #    left = ' '.join([self.label,
    #                     str(self.value).rjust(self.digits),
    #                     bar])
    #    right = '+/-, PageUp/PageDn to change, S to type'
    #    padding = ' '*(statuspanel.win.getmaxyx()[1]-len(left)-len(right))
    #    self.statuspanel.set(left + padding + right)

    def _validator(self, key, *args):
        if key == ord('q'):
            raise AbortEdit
        else:
            return key

    def text_input(self):
        _, width = self.win.getmaxyx()
        editwin = self.win.derwin(1, self.digits,
                                  0, width-self.digits)
        editwin.clrtoeol()
        b = curses.textpad.Textbox(editwin)
        curses.curs_set(1)
        try:
            b.edit(self._validator)
        except AbortEdit:
            return False
        finally:
            curses.curs_set(0)
        try:
            self.set(int(b.gather(), 0))
            return True
        except ValueError:
            return False

