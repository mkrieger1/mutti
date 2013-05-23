import curses
from panel import Panel, PanelError


class MyPanel(Panel):
    """
    Template for creating custom panels.
    """

    # uncomment this if needed, default is True
    # _focusable = False
    # _allow_children = False

    #--------------------------------------------------------------------
    # things that need to be implemented in any case
    #--------------------------------------------------------------------
    def _handle_key(self, key):
        """
        Do something depending on the key, or return the key.

        The key is not None.
        """
        raise NotImplementedError


    #--------------------------------------------------------------------
    # things that need to be implemented only if we have any children
    #--------------------------------------------------------------------
    def _update_size(self):
        """
        Calculate minimum size based on children.

        Must return a tuple (min_height, min_width).
        """
        raise NotImplementedError


    def _layout(self, height, width):
        """
        Given the window size, create subwindows for the children.

        This should also handle which children are visible, in case the
        window is too small. Use c.give_window() for each visible child c.
        """
        raise NotImplementedError


    #--------------------------------------------------------------------
    # things that can be implemented optionally
    #--------------------------------------------------------------------
    def _draw(self, height, width):
        """
        Given the available size, draw the panel.

        The children have already been drawn.
        """
        raise NotImplementedError

