from .panel import Panel


class VSpace(Panel):
    """
    Empty panel which occupies vertical space.
    """
    _max_children = 0
    _focusable = False

    def __init__(self, height):
        Panel.__init__(self, min_height=height, max_height=height,
                             max_width=0)


class HSpace(Panel):
    """
    Empty panel which occupies horizontal space.
    """
    _max_children = 0
    _focusable = False

    def __init__(self, width):
        Panel.__init__(self, min_width=width, max_width=width,
                             max_height=0)

