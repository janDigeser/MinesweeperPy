#!/usr/bin/env python3

"""
Filename: 	datastructure.py
Author:  		Jan Digeser (jan.konstantin.digeser@uni-jena.de)
Date: 		08 Mar 2018
Version: 		v0.1

Description:

    Provides the custom datastructures.
"""

import random
import typing


class Grid:
    def __init__(self, width: int, height: int, bombs: int):
        Grid._check_input(width, height, bombs)
        self.width = width
        self.height = height
        self.bombs = bombs
        self.array = [[0] * width for _ in range(height)]

    @staticmethod
    def _check_input(width, height, bombs):
        """Type-checking and checking if amount of bombs is possible"""
        if not (isinstance(width, int) and width > 1):
            raise ValueError("width has to be an integer greater than 1")
        if not (isinstance(height, int) and height > 1):
            raise ValueError("height has to be an integer greater than 1")
        if not (bombs + 9 <= width * height):
            raise ValueError("not enough space to place bombs")
        if not (bombs > 0):
            raise ValueError("bombs has to be > 0")

    def place_bombs(self, x_click: int, y_click: int):
        """Randomly places the bombs in the grid, but leaves a 3x3 square around the first click free"""
        width = len(self.array[0])
        height = len(self.array)
        # Set of the indices in the starting 3x3 square
        critical_region = set(y * width + x for x, y in self._neighbours(x_click, y_click))
        critical_region |= {y_click * width + x_click}
        # Randomly choosing over all w*h indices without the critical region
        placeholder = random.sample(set(range(width * height)) - critical_region, self.bombs)
        for place in placeholder:
            x, y = place % width, place // width        # conversion from 1d-index to 2d-indices
            self.array[y][x] = -1                       # bombs are indicated by -1
            for (x_n, y_n) in self._neighbours(x, y):   # increment the bomb counter of the neighbours
                if self.array[y_n][x_n] >= 0:           # if it itself is not a bomb
                    self.array[y_n][x_n] += 1

    def _neighbours(self, x: int, y: int) -> typing.Iterator[int]:
        """Returns Iterator over the indices of the neighbouring cells"""
        for i, j in {(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)}:
            if (0 <= (x + i) < self.width) and (0 <= (y + j) < self.height):
                yield (x + i, y + j)

    def __str__(self):
        out = "Minesweeper-Grid ({w} x {h}), Bombs: {b}\n".format(w=self.width, h=self.height, b=self.bombs)
        lines = []
        for y in self.array:
            lines.append("\n" + " ".join("{: d}".format(i) for i in y))
        out += "".join(lines)
        out = out.replace("-1", " X")
        return out + "\n"
