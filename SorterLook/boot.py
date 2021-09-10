class BootScreen:
    def __init__(self, window: any, height: int, width: int, curses) -> None:
        self.window = window
        self.width = width
        self.height = height
        self.curses = curses
        self.showContent()
        self.window.refresh()

    def showContent(self):
        content = ('<SorterLook>', 'A program that visualizes different sorting algorithms.', 'https://github.com/FFFFFF-base16/SorterLook')
        startPos = 0
        self.window.attron(self.curses.color_pair(1))
        
        for line in content:
            line = line.center(self.width)
            self.window.addstr(startPos, 0, line)
            self.window.attroff(self.curses.color_pair(1))
            startPos += 1