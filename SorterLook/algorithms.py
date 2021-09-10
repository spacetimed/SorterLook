class Loop:
    def __init__(self, window: any, curses: any, height: int, width: int, type: str) -> None:
        self.curses: any = curses
        self.window: self.curses._CursesWindow = window
        self.height: int = height
        self.width: int = width
        i = 0
        k = 0
        while k != ord('q'):
            if(i <= 100000):
                self.window.addstr(0, 0, str(i))
            k = self.window.getch()
            i += 1