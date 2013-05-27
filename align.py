from panel import Panel

class _Align(Panel):
    _max_children = 1
    _focusable = False

    def _handle_key(self, key):
        return key

    def _erase(self, height, width):
        self.win.erase()


class VAlign(_Align):
    """
    Panel for vertical alignment of one child panel.
    """
    def __init__(self, height=None, align='top'):
        Panel.__init__(self, min_height=height, max_height=height,
                             max_width=0)
        self.align = align

    def _get_size(self):
        c = self.children[0]
        height = max(self.max_height, c.max_height)
        return (height, c.min_width,
                height, c.max_width)

    def _layout(self, height, width):
        c = self.children[0]
        c.give_window(align_ver=self.align)


class HAlign(_Align):
    """
    Panel for horizontal alignment of one child panel.
    """
    def __init__(self, width=None, align='left'):
        Panel.__init__(self, min_width=width, max_width=width,
                             max_height=0)
        self.align = align

    def _get_size(self):
        c = self.children[0]
        width = max(self.max_width, c.max_width)
        return (c.min_height, width,
                c.max_height, width)

    def _layout(self, height, width):
        c = self.children[0]
        c.give_window(align_hor=self.align)
