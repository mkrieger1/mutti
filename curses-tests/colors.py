"""
Program for testing the colors and display attributes of the terminal.

While running, the display attributes (bold, reversed, blinking, etc.) can
be toggled by pressing the 0-7 keys.
"""
import curses


def init_pairs():
    for i in range(curses.COLORS):
        curses.init_pair(i, i, -1)

def show_colors(stdscr, attr):
    for i in range(curses.COLORS):
        stdscr.addstr(i, 0,
          "color pair %i" % i, (attr<<16)|curses.color_pair(i))

def show_attr(stdscr, offset):
    attrs = [(x, name) for (name, x) in curses.__dict__.iteritems()
                       if (name.startswith("A_") and
                           (x==0 or (x>0xFFFF and x<0x1000000)))]
    for (i, (x, name)) in enumerate(sorted(attrs)):
        try:
            stdscr.addstr(offset+i, 0, "%s %08X" % (name.rjust(12), x))
        except curses.error:
            pass


def main(stdscr):
    curses.curs_set(0)
    curses.use_default_colors()
    init_pairs()

    attr = 0
    while 1:
        stdscr.clear()
        show_colors(stdscr, attr)
        attr_bin = [(attr>>i) & 1 for i in range(8)]
        stdscr.addstr(10, 0, "attr %s" % attr_bin)
        show_attr(stdscr, 12)

        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key in map(ord, '01234567'):
            attr ^= (1<<int(chr(key)))


if __name__=='__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass

