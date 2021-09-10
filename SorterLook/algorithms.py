import time
import concurrent.futures
import random
import sys

import random
from typing import Dict, Callable, Type, Optional, List, Union, Tuple
from concurrent.futures.thread import ThreadPoolExecutor

import SorterLook.logging

#     author:  https://github.com/FFFFFF-base16/SorterLook/  - (2021; MIT License)
# references: https://realpython.com/sorting-algorithms-python/
#              https://docs.python.org/3/library/curses.html
#             https://docs.python.org/3.6/library/typing.html
#              https://docs.python.org/3/library/concurrent.futures.html

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
        self.sortComplete: bool = False
        self.activeColumn: int = 0
        self.AlgorithmTable: Dict[str, Callable[[None], None]] = {
            'bubble' : self.handleBubbleSort,
            'insertion' : self.handleInsertionSort,
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
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            _DisplayFuture: ThreadPoolExecutor = executor.submit(self.handleRenderDisplay)
            _SortFuture: ThreadPoolExecutor = executor.submit(self.AlgorithmTable[self.type])

    def handleRenderDisplay(self) -> None:
        while self.running:
            if self.rangeMatrix is None:
                self.rangeMatrix = [x for x in range(16)]
                random.shuffle(self.rangeMatrix)
                self.showProgress('working')
            if self.sortComplete:
                self.showProgress('complete')
            else:
                self.displayMatrix = self.getDisplayMatrix(self.rangeMatrix)
                y: int = 1
                x: int = 8
                x_0: int = x
                x_i: int = 0
                for line in self.displayMatrix:
                    for col in line:
                        if col > 0:
                            self.window.attron(self.curses.color_pair(1))
                            if x_i == self.activeColumn:
                                self.window.attron(self.curses.color_pair(3))
                        self.window.addstr(y + 1, x, str(' ') * 3)
                        self.window.attroff(self.curses.color_pair(3))
                        self.window.attroff(self.curses.color_pair(1))
                        x += 3
                        x_i += 1
                    y += 1
                    x = x_0
                    x_i = 0
                self.window.refresh()
                time.sleep(0.1)
        self.destroyWindow()

    def destroyWindow(self, error: bool = False) -> Optional[None]:
        self.curses.endwin()
        time.sleep(0.1)
        print('Exiting...')
        time.sleep(1)

    def showProgress(self, type: str) -> None:
        if(type == 'working'):
            self.window.attron(self.curses.color_pair(4))
            self.window.addstr(self.height - 2, 2, f'{self.type.title()} Sort in progress...'.center(self.width - 5))
            self.window.attroff(self.curses.color_pair(4))
        elif(type == 'complete'):
            self.window.attron(self.curses.color_pair(3))
            self.window.addstr(self.height - 2, 2, f'{self.type.title()} Sort Complete!'.center(self.width - 5))
            self.window.attroff(self.curses.color_pair(3))
            self.window.refresh()

    def handleBubbleSort(self) -> None:
        if self.rangeMatrix is not None:
            n: int = len(self.rangeMatrix)
            for i in range(n-1):
                for j in range(0, n-i-1):
                    self.activeColumn = j + 1
                    if self.rangeMatrix[j] > self.rangeMatrix[j + 1] :
                        self.rangeMatrix[j], self.rangeMatrix[j + 1] = self.rangeMatrix[j + 1], self.rangeMatrix[j]
                    time.sleep(0.1)
                    if not self.running:
                        break
                if not self.running:
                    break
            self.sortComplete = True

    def handleInsertionSort(self) -> None:
        for i in range(1, len(self.rangeMatrix)):
            item = self.rangeMatrix[i]
            j = i - 1
            while j >= 0 and self.rangeMatrix[j] > item:
                self.rangeMatrix[j + 1] = self.rangeMatrix[j]
                j -= 1
                self.activeColumn = j
                time.sleep(0.1)
            self.rangeMatrix[j + 1] = item
            time.sleep(0.1)
        self.sortComplete = True

    def getDisplayMatrix(self, matrix: list) -> List[List]:
        lenL: int = len(matrix)
        maxL: int = max(matrix)
        r: List[List] = [[0] * lenL for i in range(maxL)]
        for i in range(lenL):
            for j in range(maxL):
                if matrix[i] > j:
                    r[maxL - j - 1][i] = 1
        return r