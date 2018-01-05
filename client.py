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
		
		
# To Receive the data packet from another clients via through server
# Data packet consists of the number (ir) and the position of the number in grid (xr,xy)
def recivepacket(board):
    PacketToRecive = packetchhecker()
    wav.PlaySound("beep.wav", wav.SND_ASYNC)
    # print"Packet of Data Transmitted from Client 2 is = ", PacketToRecive
    countplayer2 = +1
    ir = int(PacketToRecive[0])
    xr = int(PacketToRecive[1])
    yr = int(PacketToRecive[2])
    board.set(xr, yr, ir, lock=True)


# To Determine the color
def rgb(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)
	
	# Class to build the GUI for sudoku games,
# some part of the class is open source code taken from https://codereview.stackexchange.com/questions/10908/python-sudoku-gui
class SudokuGUI(Frame):
    board_generators = {"SudoGen v1 (Very Easy)": sudogen_1}
    board_generator = staticmethod(sudogen_1)

    # To begin new game by clear the board
    def new_game(self):
        self.board.clear()
        self.board_generator(self.board)
        self.sync_board_and_canvas()

    def query_board(self):
        window = self.make_modal_window("Exit")
        sys.exit()

    # To make a grid
    def make_grid(self):
        global coun1

        c = Canvas(self, bg=rgb(68, 90, 235), width='512', height='512')
        ###################################### Labels TO initilaize Players
        widget = Label(c, text='Player 1', fg='yellow', bg='black')
        widget.pack()
        c.create_window(575, 35, window=widget)
        c.pack(side='top', fill='both', expand='5')

        widget = Label(c, text='Player 2', fg='yellow', bg='black')
        widget.pack()
        c.create_window(575, 200, window=widget)
        c.pack(side='top', fill='both', expand='5')
        ################################# Labels For Naick Names of Players
        widget = Label(c, text='Nickname', fg='yellow', bg='black')
        widget.pack()
        c.create_window(575, 60, window=widget)
        c.pack(side='top', fill='both', expand='10')

        widget = Label(c, text='Nickname', fg='yellow', bg='black')
        widget.pack()
        c.create_window(575, 225, window=widget)
        c.pack(side='top', fill='both', expand='5')

        self.rects = [[None for x in range(9)] for y in range(9)]
        self.handles = [[None for x in range(9)] for y in range(9)]
        rsize = 512 / 9
        guidesize = 512 / 3
        Label(tk,
              text=" Sudoku Game",
              fg="blue",
              font="Verdana 10 bold").pack()
        Label(tk,
              text="Institute of Computer Science, University of Tartu",
              fg="blue",
              font="Verdana 10 bold").pack()

        for y in range(9):
            for x in range(9):
                (xr, yr) = (x * guidesize, y * guidesize)
                self.rects[y][x] = c.create_rectangle(xr, yr, xr + guidesize,
                                                      yr + guidesize, width=10, )
                (xr, yr) = (x * rsize, y * rsize)
                r = c.create_rectangle(xr, yr, xr + rsize, yr + rsize)
                t = c.create_text(xr + rsize / 2, yr + rsize / 2, text="TIME",
                                  font="System 15 bold")
                self.handles[y][x] = (r, t)
        self.canvas = c
        self.sync_board_and_canvas()

    # To check the number and store it in the gride
    #################################################################################################
