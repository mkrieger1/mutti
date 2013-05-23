import curses
import curses.textpad
from panel import Panel

class Dial(Panel):
    """A widget to display and manipulate one numeric value."""

    def __init__(self, label, value, vrange, statuspanel):
        self.label_width = label[1]
        self.value_digits = value[1]
        width = self.label_width + self.value_digits + 1
        Panel.__init__(self, min_height=1, min_width=width,
                             max_height=1, max_width=width)

        self.vmin, self.vmax = vrange
        self.step = 10
        self.set(value[0])

        self.label_text = label[0]
        self.statuspanel = statuspanel
        self.has_focus = False

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

    def set_status(self):
        bar_len = 20
        bar_pos = ((self.value - self.vmin) * bar_len / 
                   (self.vmax  - self.vmin))
        bar = '#'*bar_pos + '-'*(bar_len-bar_pos)
        left = ' '.join([self.label_text,
                         str(self.value).rjust(self.value_digits),
                         bar])
        right = '+/-, PageUp/PageDn to change, S to type'
        padding = ' '*(statuspanel.win.getmaxyx()[1]-len(left)-len(right))
        self.statuspanel.set(left + padding + right)

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

    def _erase(self, height, width):
        self.win.erase()

    def _draw(self, height, width):
        self.addstr(0, 0, self.label_text)
        self.addstr(0, self.label_width,
                    str(self.value).rjust(self.value_digits),
                    curses.A_REVERSE if self.has_focus else curses.A_NORMAL)
        # TODO handle size < min_size

    def _handle_key(self, key):
        if key == ord('+'):
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

