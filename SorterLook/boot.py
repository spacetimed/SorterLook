from typing import Tuple


class BootScreen:
    def __init__(self, curses, window: any, height: int, width: int) -> None:
        self.width: int = width
        self.height: int = height
        self.curses: any = curses
        self.window: self.curses._CursesWindow = window

        self.showContent()

    def showContent(self) -> None:
        content: Tuple = ('<SorterLook>', 'A program that visualizes different sorting algorithms.', 'https://github.com/FFFFFF-base16/SorterLook')
        startPos: int = 0
        self.window.attron(self.curses.color_pair(1))
        
        for line in content:
            line: str = line.center(self.width)
            self.window.addstr(startPos, 0, line)
            self.window.attroff(self.curses.color_pair(1))
            startPos += 1
            
        self.window.refresh()