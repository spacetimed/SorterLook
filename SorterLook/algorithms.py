from typing import Dict, Callable, Type

import concurrent.futures
import random
import time

class Loop:
    def __init__(self, curses: any, window: any, height: int, width: int, type: str) -> None:
        self.curses: any = curses
        self.window: self.curses._CursesWindow = window
        self.height: int = height
        self.width: int = width
        self.running: bool = False

        self.mainLoop()

    def mainLoop(self):
        self.running = True

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(self.output)
            executor.submit(self.keyListener)

    def output(self) -> None:
        i = 0
        while self.running:
            self.window.addstr(7, 5, f'output')
            self.window.refresh()
            i += 1

    def keyListener(self) -> None:
        k = 0
        while k != ord('q'):
            k = self.window.getch()
        self.running = False