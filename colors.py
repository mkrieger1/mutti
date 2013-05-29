import curses

_pairs = {(-1, -1): 0}

def color_attr(fg=None, bg=None):
    global _pairs

    # check if curses.use_default_colors() was called
    use_default_colors = True
    try:
        curses.init_pair(0, -1, -1)
    except curses.error:
        use_default_colors = False

    # replace defaults
    fg = fg or (-1 if use_default_colors else "white")
    bg = bg or (-1 if use_default_colors else "black")

    # convert color names to numbers
    # available names:
    # black, blue, cyan, green, magenta, red, white, yellow
    if isinstance(fg, str):
        fg = getattr(curses, "COLOR_"+fg.upper())
    if isinstance(bg, str):
        bg = getattr(curses, "COLOR_"+bg.upper())

    # create new pair if needed and return pair number
    if (fg, bg) not in _pairs:
        curses.init_pair(len(_pairs), fg, bg)
        _pairs[(fg, bg)] = len(_pairs)
    return curses.color_pair(_pairs[(fg, bg)])
    
