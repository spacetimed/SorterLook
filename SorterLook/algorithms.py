import time
import concurrent.futures
import random
import sys

from typing import Dict, Callable, Type, Optional, List
from concurrent.futures.thread import ThreadPoolExecutor


class Loop:
    def __init__(self, curses: any, window: any, height: int, width: int, type: str) -> None:
        self.curses: any = curses
        self.window: self.curses._CursesWindow = window
        self.height: int = height
        self.width: int = width
        self.running: bool = False
        self.k: int = 0
        try:
            self.mainLoop()
        except KeyboardInterrupt:
            self.running = False

    def mainLoop(self):
        self.running = True
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(self.output)
            executor.submit(self.keyListener)

    def output(self) -> Optional[str]:
        i = 0
        while self.running:
            self.window.addstr(7, 5, f'output')
            self.window.refresh()
            i += 1
        self.curses.endwin()
        time.sleep(0.1)
        print('Quitting')
        time.sleep(1)

    def keyListener(self) -> Optional[str]:
        while (self.k != ord('q')) and (self.running):
            self.k = self.window.getch()
        self.running = False