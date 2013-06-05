import curses
import curses.ascii
from panel import Panel
from util import distribute_space


class Grid(Panel):
    """
    Arrange panels in a grid.
    """
    def __init__(self, rows, columns):
        Panel.__init__(self)
        self._rows = rows
        self._columns = columns
        self._align_hor = {}
        self._align_ver = {}
        self._pos = {}
        self._panel = {}


    def adopt(self, panel, row, col, align_hor='left', align_ver='top',
                    update_size=True):
        pos = (row, col)
        self._pos[panel] = pos
        self._panel[pos] = panel
        Panel.adopt(self, panel, update_size)
        self._align_hor[pos] = align_hor
        self._align_ver[pos] = align_ver
        self.children.sort(key=lambda c: self._pos[c])

    #--------------------------------------------------------------------

    def _handle_key(self, key):
        if key in [curses.ascii.TAB, ord('w')]:
            if not self.focus_next():
                return key
        elif key in [curses.KEY_BTAB, ord('b')]:
            if not self.focus_prev():
                return key
        elif key in [curses.KEY_DOWN, ord('j')]:
            if not self.focus_down():
                return key
        elif key in [curses.KEY_UP, ord('k')]:
            if not self.focus_up():
                return key
        elif key in [curses.KEY_LEFT, ord('h')]:
            if not self.focus_left():
                return key
        elif key in [curses.KEY_RIGHT, ord('l')]:
            if not self.focus_right():
                return key
        else:
            return key


    def _move_focus_grid(self, ver, hor):
        row, col = self._pos[self.focused_child]
        while True:
            row += ver
            col += hor
            if (row not in range(self._rows) or
                col not in range(self._columns)):
                return False
            for (i, c) in enumerate(self.children):
                if self._pos[c] == (row, col):
                    if self._move_focus_to(i):
                        return True
    def focus_down(self):
        return self._move_focus_grid(1, 0)
    def focus_up(self):
        return self._move_focus_grid(-1, 0)
    def focus_left(self):
        return self._move_focus_grid(0, -1)
    def focus_right(self):
        return self._move_focus_grid(0, 1)

    #--------------------------------------------------------------------

    def _row_min_height(self, row):
        return max([0]+[c.min_height for c in self.children
                        if self._pos[c][0] == row])

    def _row_max_height(self, row):
        return max([0]+[c.max_height for c in self.children
                        if self._pos[c][0] == row])

    def _col_min_width(self, col):
        return max([0]+[c.min_width for c in self.children
                        if self._pos[c][1] == col])

    def _col_max_width(self, col):
        return max([0]+[c.max_width for c in self.children
                        if self._pos[c][1] == col])


    def _get_size(self):
        min_height = sum(self._row_min_height(row)
                         for row in range(self._rows))
        min_width  = sum(self._col_min_width(col)
                         for col in range(self._columns))
        max_height = sum(self._row_max_height(row)
                         for row in range(self._rows))
        max_width  = sum(self._col_max_width(col)
                         for col in range(self._columns))
        return (min_height, min_width, max_height, max_width)


    def _layout(self, height, width):
        give_row = [self._row_min_height(row)
                    for row in range(self._rows)]
        want_row = [self._row_max_height(row)-self._row_min_height(row)
                    for row in range(self._rows)]
        give_col = [self._col_min_width(col)
                    for col in range(self._columns)]
        want_col = [self._col_max_width(col)-self._col_min_width(col)
                    for col in range(self._columns)]
        idx_row, idx_col = self._pos[self.focused_child]

        distribute_space(height, idx_row, give_row, want_row)
        distribute_space(width,  idx_col, give_col, want_col)
        # TODO scrolling arrows

        top = 0
        for row in range(self._rows):
            h = give_row[row]
            left = 0
            for col in range(self._columns):
                w = give_col[col]
                if (row, col) in self._panel:
                    c = self._panel[(row, col)]
                    if h > 0 and w > 0:
                        c.give_window(h, w, top, left)
                    else:
                        c.take_window()
                left += w
            top += h


    def _erase(self, height, width):
        self.win.erase()

