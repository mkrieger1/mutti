import curses
import curses.ascii
from panel import Panel
from colors import color_attr


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
        self.state = False
        self.label = label
        self._draw_label = draw_label


    def _handle_key(self, key):
        if key == ord('y'):
            self.state = True
            return curses.ascii.TAB # focus next
        elif key == ord('n'):
            self.state = False
            return curses.ascii.TAB
        elif key == curses.ascii.SP:
            self.state = not self.state
        else:
            return key


    def _erase(self, height, width):
        self.win.erase()
            

    def _draw(self, height, width):
        attr = curses.A_BOLD if self.has_focus else curses.A_NORMAL

        if self._draw_label:
            labelstr = self.label
            if len(labelstr) > width-1:
                labelstr = labelstr[:width-2]+'~'
            self.addstr(0, 0, labelstr, attr)

        statestr = 'X' if self.state else '-'
        self.addstr(0, width-1, statestr, attr|color_attr("yellow"))


    def _get_status_draw_task(self):
        def status_draw_task(statusbar):
            _, width = statusbar.win.getmaxyx()
            statusbar.win.erase()
            statustext = "%s: %s" % (self.label,
                                     "ON" if self.state else "OFF")
            statusbar.addstr(0, 0, statustext, curses.A_BOLD)
            helptext = "Space to toggle, Y/N to set"
            if len(statustext) + len(helptext) < width:
                statusbar.addstr(0, width-len(helptext), helptext)
        return status_draw_task

