class BootScreen:
    def __init__(self, window: any, height: int, width: int, curses) -> None:
        self.window = window
        self.width = width
        self.height = height
        self.curses = curses
        self.showLogo()
        self.window.refresh()

    def showLogo(self):
        logo = """<SorterLook>
A program that visualizes different sorting algorithms.
author: @FFFFFF-base16 (GitHub) - 2021"""
        startPos = 0
        self.window.attron(self.curses.color_pair(1))
        
        for line in logo.splitlines():
            line = line.center(self.width)
            self.window.addstr(startPos, 0, line)
            self.window.attroff(self.curses.color_pair(1))
            startPos += 1