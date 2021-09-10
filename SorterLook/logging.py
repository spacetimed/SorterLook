from typing import Optional

class Logger:
    def __init__(self, name: str, curses: any, window: any, height: int, width: int) -> None:
        self.name = name
        self.curses: any = curses
        self.window: self.curses._CursesWindow = window
        self.height: int = height
        self.width: int = width

    def __call__(self, message: str) -> Optional[bool]:
        message = message.center(self.width)
        self.window.attron(self.curses.color_pair(2))
        self.window.addstr(self.height - 11, 0, message)
        self.window.addstr(self.height - 10, 0, 'Program will exit in 5 seconds.'.center(self.width))
        self.window.attroff(self.curses.color_pair(2))
        self.window.refresh()
        return