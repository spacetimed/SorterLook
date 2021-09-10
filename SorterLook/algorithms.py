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
        self.key: int = 0

        self.AlgorithmTable = {
            'bubble' : self.handleBubbleSort,
        }

        try:
            self.mainLoop()
        except KeyboardInterrupt:
            self.running = False

    def mainLoop(self) -> None:
        self.running = True
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            DisplayFuture: ThreadPoolExecutor = executor.submit(self.handleBubbleSort)
            KeyListenerFuture: ThreadPoolExecutor = executor.submit(self.keyListener)

    def displayHandler(func) -> None:
        def displayWrapper(self):
            i = 0
            while self.running:
                func(self)
                self.window.refresh()
                time.sleep(0.1)
                i += 1
            self.handleQuit()
        return displayWrapper

    @displayHandler
    def handleBubbleSort(self) -> None:
        self.window.addstr(7, 5, f'handleBubbleSort')

    def handleQuit(self) -> None:
        self.curses.endwin()
        time.sleep(0.1)
        print('Quitting')
        time.sleep(1)

    def keyListener(self) -> None:
        while (self.key != ord('q')) and (self.running):
            self.key = self.window.getch()
        self.running = False