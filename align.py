from panel import Panel, INF

class VAlign(Panel):
    """
    Panel for vertical alignment of one child panel.
    """
    _max_children = 1

    def __init__(self, height=None, align_ver='top'):
        Panel.__init__(self, min_height=height, max_height=height,
                             max_width=0)
        self.align_ver = align_ver

    def _handle_key(self, key):
        return key

    def _get_size(self):
        c = self.children[0]
        height = max(self.max_height, c.max_height)
        return (height, c.min_width,
                height, c.max_width)

    def _layout(self, height, width):
        c = self.children[0]
        c.give_window(align_ver=self.align_ver)

    def _erase(self, height, width):
        self.win.erase()

