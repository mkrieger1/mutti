import curses
import curses.ascii
from panel import Panel
from colors import color_attr
from util import shorten_label


class Toggle(Panel):
    """
    A panel to toggle between a two states.
    """

    _max_children = 0

    def __init__(self, label="", draw_label=True, min_width=None, max_width=None):
        if min_width is None:
            if label and draw_label:
                min_width = len(label)+2
            else:
                min_width = 1
        max_width = max_width or min_width
        Panel.__init__(self, min_height=1, min_width=min_width,
                             max_height=1, max_width=max_width)
        self.set_state(False)
        self.label = label
        self._draw_label = draw_label


    def _handle_key(self, key):
        if key == ord('y'):
            self.set_state(True)
            return curses.ascii.TAB # focus next
        elif key == ord('n'):
            self.set_state(False)
            return curses.ascii.TAB
        elif key == curses.ascii.SP:
            self.set_state(not self.state)
        else:
            return key

    def _displaytext(self):
        return 'X' if self.state else '-'

    def _statustext(self):
        return 'ON' if self.state else 'OFF'

    def _helptext(self):
        return "Space to toggle, Y/N to set"

    def _erase(self, height, width):
        self.win.erase()
            

    def _draw(self, height, width):
        attr = curses.A_BOLD if self.has_focus else curses.A_NORMAL

        changed = self._changed()
        if self._draw_label:
            labelstr = shorten_label(self.label, width-2)
            c = color_attr("blue") if changed else 0
            self.addstr(0, 0, labelstr, attr|c)

        statestr = self._displaytext()
        c = (color_attr("blue") if changed else color_attr("yellow"))
        self.addstr(0, width-1, statestr, attr|c)


    def _get_status_draw_task(self):
        def status_draw_task(statusbar):
            _, width = statusbar.win.getmaxyx()
            statusbar.win.erase()
            statustext = "%s: %s" % (
                self.label.strip() + ("*" if self._changed() else ""),
                self._statustext())
            statusbar.addstr(0, 0, statustext, curses.A_BOLD)
            helptext = self._helptext()
            if len(statustext) + len(helptext) < width:
                statusbar.addstr(0, width-len(helptext), helptext)
        return status_draw_task


    def _changed(self):
        """
        Indicate whether the state differs from the last known state.
        """
        return False # overwrite me!

    #--------------------------------------------------------------------

    def set_state(self, state):
        self.state = bool(state)

