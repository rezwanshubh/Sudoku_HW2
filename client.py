import socket
import threading
import select
import random
import time
import winsound
import winsound as wav
import tkMessageBox
import Tkinter
from Tkinter import *
import tkMessageBox
import pika
import uuid
import Queue
from easygui import *

exiting = False
random.seed(time.time())

global Randomnumber
global Checker
global increment
global nickname
nickname = ''

# Initialise a global variables
coun1 = 0
increment = 0


class SudokuBoard:
    def __init__(self):
        self.clear()

    # To clear the grid
    def clear(self):
        self.grid = [[0 for x in range(9)] for y in range(9)]
        self.locked = []

    # To get the numbers from rows
    def get_row(self, row):
        return self.grid[row]

    # To get the numbers from columns
    def get_cols(self, col):
        return [y[col] for y in self.grid]

    # To get numbers from the subgrids
    def get_nearest_region(self, col, row):
        def make_index(v):
            if v <= 2:
                return 0
            elif v <= 5:
                return 3
            else:
                return 6

        return [y[make_index(col):make_index(col) + 3] for y in
                self.grid[make_index(row):make_index(row) + 3]]

    # To set the numbers into the subgrids
    def set(self, col, row, v, lock=False):
        if v == self.grid[row][col] or (col, row) in self.locked:
            return
        for v2 in self.get_row(row):
            if v == v2:
                raise ValueError()
        for v2 in self.get_cols(col):
            if v == v2:
                raise ValueError()
        for y in self.get_nearest_region(col, row):
            for x in y:
                if v == x:
                    raise ValueError()
        self.grid[row][col] = v
        if lock:
            self.locked.append((col, row))
			
	def get(self, col, row):
        return self.grid[row][col]

    def __str__(self):
        strings = []
        newline_counter = 0
        for y in self.grid:
            strings.append("%d%d%d %d%d%d %d%d%d" % tuple(y))
            newline_counter += 1
            if newline_counter == 3:
                strings.append('')
                newline_counter = 0
        return '\n'.join(strings)
