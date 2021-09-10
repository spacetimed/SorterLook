import curses

import SorterLook.boot
#import SorterLook.logging


class Start:
    def __init__(self,
                 type: str
                 ) -> None:

        self.type: str = type

        self.width: int = 70
        self.height: int = 20
        self.bootHeight: int = 4

        self.window: curses._CursesWindow = None
        self.bootWindow: curses._CursesWindow = None
        self.helpWindow: curses._CursesWindow = None

        curses.wrapper(self.main)

    def main(self, stdscr) -> None:
        self.stdscr: any = stdscr

        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        self.bootWindow = curses.newwin(
            self.bootHeight, self.width,  0,  0)
        self.bootWindow.border(' ', ' ', ' ', '_', ' ', ' ', '_', '_')
        self.bootScreen = SorterLook.boot.BootScreen(self.bootWindow,
                                                     self.bootHeight,
                                                     self.width,
                                                     curses=curses)

        self.window = curses.newwin(
            self.height,  self.width,  self.bootHeight - 1,  0)
        self.window.border(' ', ' ', '_', '_', '_', '_', '_', '_')
        self.window.refresh()

        self.helpWindow = curses.newwin(
            2,  self.width,  self.bootHeight + self.height - 1,  0)
        self.helpWindow.border(' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ')
        self.helpWindow.attron(curses.color_pair(1))
        self.helpWindow.addstr(0, 0, 'Press q to exit.'.center(self.width))
        self.helpWindow.attroff(curses.color_pair(1))
        self.helpWindow.refresh()

        self.window.nodelay(True)

        k = 0
        while k != ord('q'):
            self.window.refresh()
            k = self.window.getch()
