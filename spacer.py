import curses
from panel import Panel, PanelError


class Spacer(Panel):
    """
    Empty panel used as spacer.
    """

    _focusable = False
    _allow_children = False

