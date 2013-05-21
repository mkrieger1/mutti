import curses
import curses.textpad
from panel import Panel

class Dial(Panel):
    """A widget to display and manipulate one numeric value."""

    def __init__(self, parent, pos, label, value, vrange):
        self.label_width = label[1]
        self.value_digits = value[1]
        width = self.label_width + self.value_digits + 1
        Panel.__init__(self, parent, pos, (1, width))

        self.vmin, self.vmax = vrange
        self.step = 10
        self.set(value[0])

        self.label_text = label[0]
        self.focused = False

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

    def set_status(self, statuspanel):
        bar_len = 20
        bar_pos = ((self.value - self.vmin) * bar_len / 
                   (self.vmax  - self.vmin))
        bar = '#'*bar_pos + '-'*(bar_len-bar_pos)
        left = ' '.join([self.label_text,
                         str(self.value).rjust(self.value_digits),
                         bar])
        right = '+/-, PageUp/PageDn to change, S to type'
        padding = ' '*(statuspanel.width-len(left)-len(right))
        statuspanel.set(left + padding + right)

    def text_input(self):
        editwin = self.win.derwin(1, self.value_digits+1,
                                  0, self.label_width)
        editwin.clrtoeol()
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
                    curses.A_REVERSE if self.is_focused else curses.A_NORMAL)

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
        elif key == ord('s'):
            self.text_input()
        else:
            return key


class DialList(Panel):
    """A widget to display and manipulate multiple numeric values."""

    def __init__(self, parent, pos, title):
        Panel.__init__(self, parent, pos, (0, 0))
        self.dials = []
        self.title = title
        self.focused = 0

    def add_dial(self, label, value, vrange):
        pos = (len(self.dials)+1, 0)
        d = Dial(self.win, pos, label, value, vrange)
        self.dials.append(d)
        self.dials[self.focused].focused = True
        self.height = len(self.dials)+1
        self.width = max([d.width for d in self.dials] + [len(self.title)])

    def set_focus(self, i):
        self.dials[self.focused].focused = False
        self.focused = i % len(self.dials)
        self.dials[self.focused].focused = True

    def focus_next(self):
        self.set_focus(self.focused + 1)

    def focus_prev(self):
        self.set_focus(self.focused - 1)

    def set_status(self, statuspanel):
        self.dials[self.focused].set_status(statuspanel)

    def draw(self):
        self.addstr(0, 0, self.title, curses.A_BOLD)
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
        else:
            return self.dials[self.focused].handle_key(key)
