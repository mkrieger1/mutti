import curses
import panel

class Button(panel.Panel):
    def __init__(self, parent, top, left, height, width, text):
        panel.Panel.__init__(self, parent, top, left, height, width)
        self.text = text
        self.focus = False

    def draw(self):
        height, width = self.win.getmaxyx()
        vcenter = (height-1)/2
        hcenter = (width-1)/2+1
        hbeginstr = hcenter - len(self.text)/2 - 1

        # print text
        text = ' '+self.text+' '
        attr = curses.A_REVERSE if self.focus else curses.A_NORMAL
        self.addstr(vcenter, hbeginstr, text, attr)

        # print shadow
        for x in range(width-1):
            self.addch(height-1, x, curses.color_pair(1))

