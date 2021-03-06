import curses
import curses.textpad
import curses.ascii
from .panel import Panel
from .colors import color_attr
from .util import shorten_label


class AbortEdit(Exception):
    pass


class Dial(Panel):
    """A widget to display and manipulate one numeric value."""

    _max_children = 0

    def __init__(self, vrange, digits, label="", draw_label=True,
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
        self.set_value(value)

        self.label = label
        self._draw_label = draw_label

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

    def _displaytext(self):
        return str(self.value)

    def _statustext(self):
        return str(self.value)

    def _statuslabel(self):
        return self.label

    def _helptext(self):
        return "+/-/^A/^X, PgUp/PgDn/^U/^D to change, S to type"

    def _erase(self, height, width):
        self.win.erase()

    def _draw(self, height, width):
        attr = curses.A_BOLD if self.has_focus else curses.A_NORMAL

        labelstr = self.label
        valuestr = self._displaytext()

        changed = self._changed()
        w = len(valuestr)+1
        if self._draw_label:
            labelstr = shorten_label(labelstr, width-w)
            c = color_attr("blue") if changed else 0
            self.addstr(0, 0, labelstr, attr|c)
        else:
            labelstr = ""

        if len(valuestr) < width-len(labelstr):
            c = (color_attr("blue") if changed else color_attr("yellow"))
            self.addstr(0, width-len(valuestr), valuestr,
                        attr|c)

    def _get_status_draw_task(self):
        def status_draw_task(statusbar):
            _, width = statusbar.win.getmaxyx()
            statusbar.win.erase()
            statustext = "%s: %s" % (
                self._statuslabel().strip() + ("*" if self._changed() else ""),
                self._statustext())
            statusbar.addstr(0, 0, statustext, curses.A_BOLD)
            helptext = self._helptext()
            if len(statustext) + len(helptext) < width:
                statusbar.addstr(0, width-len(helptext), helptext)
        return status_draw_task

    #--------------------------------------------------------------------

    def set_value(self, value):
        if value > self.vmax:
            self.value = self.vmax
        elif value < self.vmin:
            self.value = self.vmin
        else:
            self.value = value

    def inc(self, amount):
        self.set_value(self.value+amount)

    def dec(self, amount):
        self.set_value(self.value-amount)

    def _validator(self, key, *args):
        if key == ord('q'):
            raise AbortEdit
        else:
            return key

    def _from_text(self, text):
        return int(text, 0)

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
            self.set_value(self._from_text(b.gather()))
            return True
        except ValueError:
            return False

    def _changed(self):
        """
        Indicate whether the value differs from the last known state.
        """
        return False # overwrite me!

