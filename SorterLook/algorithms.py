import time
import concurrent.futures
import random
import sys

from typing import Dict, Callable, Type, Optional, List
from concurrent.futures.thread import ThreadPoolExecutor

import SorterLook.logging

class Loop:
    def __init__(self, curses: any, window: any, height: int, width: int, type: str) -> None:
        self.curses: any = curses
        self.window: self.curses._CursesWindow = window
        self.height: int = height
        self.width: int = width
        self.running: bool = False
        self.key: int = 0
        self.type: str = type
        self.logger = SorterLook.logging.Logger(__name__, self.curses, self.window, self.height, self.width)

        self.AlgorithmTable = {
            'bubble' : self.handleBubbleSort,
        }

        if self.type not in self.AlgorithmTable:
            self.logger('An unknown sorting algorithm type was provided.')
            time.sleep(5)
            self.destroyWindow()
            sys.exit()

        try:
            self.mainLoop()
        except KeyboardInterrupt:
            self.running = False

    def mainLoop(self) -> None:
        self.running = True
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            _DisplayFuture: ThreadPoolExecutor = executor.submit(self.handleBubbleSort)
            _KeyListenerFuture: ThreadPoolExecutor = executor.submit(self.keyListener)

    def DisplayHandler(func) -> None:
        def displayWrapper(self):
            i = 0
            while self.running:
                func(self)
                self.window.refresh()
                time.sleep(0.1)
                i += 1
            self.destroyWindow()
        return displayWrapper

    @DisplayHandler
    def handleBubbleSort(self) -> None:
        self.window.addstr(7, 5, f'handleBubbleSort')

    def destroyWindow(self, error: bool = False) -> Optional[None]:
        self.curses.endwin()
        time.sleep(0.1)
        print('Quitting')
        time.sleep(1)

    def keyListener(self) -> None:
        while (self.key != ord('q')) and (self.running):
            self.key = self.window.getch()
        self.running = False