import curses
import curses.textpad
from panel import Panel

class Dial(Panel):
    """A widget to display and manipulate one numeric value."""

    def __init__(self, parent, pos, label, value, vrange):
        self.label_width = label[1]
        self.value_digits = value[1]
        width = self.label_width + self.value_digits
        Panel.__init__(self, parent, pos, (1, width))

        self.vmin, self.vmax = vrange
        self.step = 10
        self.set(value[0])

        self.label_text = label[0]
        self.focus = False

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

    def get_status(self):
        bar_len = 20
        bar_pos = ((self.value - self.vmin) * bar_len / 
                   (self.vmax  - self.vmin))
        bar = '#'*bar_pos + '-'*(bar_len-bar_pos)
        return ' '.join([self.label_text,
                         str(self.value).rjust(self.value_digits),
                         bar])

    def text_input(self):
        (y, x) = self.win.getparyx()
        editwin = curses.newwin(1, self.value_digits+1,
                                y, x+self.width-self.value_digits) 
        b = curses.textpad.Textbox(editwin)
        curses.curs_set(1)
        b.edit()
        curses.curs_set(0)
        try:
            self.set(int(b.gather()))
        except ValueError:
            pass

    def draw(self):
        self.addstr(0, 0, self.label_text)
        self.addstr(0, self.label_width,
                    str(self.value).rjust(self.value_digits),
                    curses.A_REVERSE if self.focus else curses.A_NORMAL)

    def handle_key(self, key):
        if key is None:
            return
        elif key == ord('+'):
            self.inc(1)
        elif key == ord('-'):
            self.dec(1)
        elif key == curses.KEY_PPAGE:
            self.inc(self.step)
        elif key == curses.KEY_NPAGE:
            self.dec(self.step)
        else:
            return key


class DialList(Panel):
    """A widget to display and manipulate multiple numeric values."""

    def __init__(self, parent, pos):
        Panel.__init__(self, parent, pos, (0, 0))
        self.dials = []
        self.focused = 0

    def add_dial(self, label, value, vrange):
        pos = (self.top+self.height, self.left)
        d = Dial(self.parent, pos, label, value, vrange)
        self.dials.append(d)
        self.dials[self.focused].focus = True
        self.height = len(self.dials)
        self.width = max(d.width for d in self.dials)

    def set_focus(self, i):
        self.dials[self.focused].focus = False
        self.focused = i % len(self.dials)
        self.dials[self.focused].focus = True

    def focus_next(self):
        self.set_focus(self.focused + 1)

    def focus_prev(self):
        self.set_focus(self.focused - 1)

    def get_status(self):
        return self.dials[self.focused].get_status()

    def draw(self):
        for d in self.dials:
            d.redraw()

    def handle_key(self, key):
        if key is None:
            return
        elif key in map(ord, map(str, range(1, len(self.dials)+1))):
            self.set_focus(int(chr(key))-1)
        elif key in [curses.KEY_DOWN, ord('j')]:
            self.focus_next()
        elif key in [curses.KEY_UP, ord('k')]:
            self.focus_prev()
        elif key == ord('s'):
            self.dials[self.focused].text_input()
            self.focus_next()
        else:
            return self.dials[self.focused].handle_key(key)

