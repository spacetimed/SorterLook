import time
import concurrent.futures
import random
import sys

from typing import Dict, Callable, Type, Optional, List, Union
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
        self.rangeMatrix: Union[List or None] = None
        self.displayMatrix: Union[None or List[List]] = None

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

    def DisplayHandlerProperty(func) -> None:
        def displayWrapper(self):
            while self.running:
                func(self)
                time.sleep(0.1)
            self.destroyWindow()
        return displayWrapper

    @DisplayHandlerProperty
    def handleBubbleSort(self) -> None:
        if self.rangeMatrix is None:
            self.rangeMatrix = [x for x in range(18)]
        self.displayMatrix = self.getDisplayMatrix(self.rangeMatrix)
        y = 0
        x = 0
        for line in self.displayMatrix:
            #bar: str = ''.join(str(x) for x in line)
            for col in line:
                if col > 0:
                    self.window.attron(self.curses.color_pair(1))
                self.window.addstr(y + 1, x, str('  '))
                self.window.attroff(self.curses.color_pair(1))
                x += 2
            y += 1
            x = 0
        self.window.refresh()

    def getDisplayMatrix(self, matrix: list) -> List[List]:
        highest: int = max(matrix)
        y_index: int = highest
        x_index: int = 0
        outputMatrix: List[List] = [[0 for i in range(len(matrix))] for j in range(highest)]
        for y in range(len(outputMatrix)):
            for x in matrix:
                if(x >= y_index):
                    outputMatrix[y][x_index] = 1
                x_index += 1
            y_index -= 1
            x_index = 0
        return outputMatrix

    def destroyWindow(self, error: bool = False) -> Optional[None]:
        self.curses.endwin()
        time.sleep(0.1)
        print('Quitting')
        time.sleep(1)

    def keyListener(self) -> None:
        while (self.key != ord('q')) and (self.running):
            self.key = self.window.getch()
        self.running = False