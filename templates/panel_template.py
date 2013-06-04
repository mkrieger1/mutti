import curses
from panel import Panel, PanelError


class MyPanel(Panel):
    """
    Template for creating custom panels.
    """

    # uncomment this if needed, default is True
    # _focusable = False

    # uncomment and change this if needed, default is INF
    # _max_children = 1

    #--------------------------------------------------------------------
    # things that need to be implemented in any case
    #--------------------------------------------------------------------
    def _handle_key(self, key):
        """
        Do something depending on the key, or return the key.

        The key is not None.
        """
        if self._focusable:
            raise NotImplementedError


    #--------------------------------------------------------------------
    # things that need to be implemented only if there are any children
    #--------------------------------------------------------------------
    def _get_size(self):
        """
        Calculate minimum and maximum size of a panel.

        Must return a tuple (min_height, min_width,
                             max_height, max_width).
        None as minimum value will be converted to 0.
        None as maximum value will be converted to INF.
        """
        if self._max_children:
            raise NotImplementedError


    def _layout(self, height, width):
        """
        Given the window size, create subwindows for the children.

        This should also handle which children are visible, in case the
        window is too small. Use c.give_window() for each visible child c.
        """
        if self._max_children:
            raise NotImplementedError


    #--------------------------------------------------------------------
    # things that can be implemented optionally
    #--------------------------------------------------------------------
    def _erase(self, height, width):
        """
        Erase the window, and draw the background.

        The children will be drawn on top.
        """
        self.win.erase()
        # draw the background
            
    def _draw(self, height, width):
        """
        Draw the foreground over the children.
        """
        pass # draw the foreground

    def _get_status_draw_task(self):
        """
        Create a function which draws onto the status bar.

        The status bar must be the only parameter of the function.
        """
        return None

