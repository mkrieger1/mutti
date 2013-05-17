import curses
import panel

class Dial(panel.Panel):
    def __init__(self, parent, pos, label, value, vrange):
        self.label_width = label[1]
        self.value_digits = value[1]
        width = self.label_width + self.value_digits
        panel.Panel.__init__(self, parent, pos, (1, width))

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


class DialList(panel.Panel):
    def __init__(self, parent, pos):
        panel.Panel.__init__(self, parent, pos, (0, 0))
        self.dials = []
        self.focused = 0

    def add_dial(self, label, value, vrange):
        pos = (self.top+self.height, self.left)
        d = Dial(self.parent, pos, label, value, vrange)
        self.dials.append(d)
        self.dials[self.focused].focus = True
        self.height = len(self.dials)
        self.width = max(d.width for d in self.dials)

    def focus_next(self):
        self.dials[self.focused].focus = False
        self.focused = (self.focused + 1) % len(self.dials)
        self.dials[self.focused].focus = True

    def focus_prev(self):
        self.dials[self.focused].focus = False
        self.focused = (self.focused - 1) % len(self.dials)
        self.dials[self.focused].focus = True

    def draw(self):
        for d in self.dials:
            d.redraw()

    def handle_key(self, key):
        if key is None:
            return
        elif key == curses.KEY_DOWN:
            self.focus_next()
        elif key == curses.KEY_UP:
            self.focus_prev()
        else:
            return self.dials[self.focused].handle_key(key)

