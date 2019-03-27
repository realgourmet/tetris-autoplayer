# Tetris Game.  Mark Handley, UCL, 2018
from enum import Enum

#switch this to True to enable autoplaying by default
DEFAULT_AUTOPLAY = False

#switch this to True to disable the GUI.  Probably not useful unless
#you default to autoplay.
DISABLE_DISPLAY = False

#settings below should not be changed
GRID_SIZE = 25
MAXROW = 20
MAXCOL = 10
CANVAS_WIDTH = GRID_SIZE * (7 + MAXCOL)
CANVAS_HEIGHT = GRID_SIZE * (4 + MAXROW)

class Direction(Enum):
    LEFT = -1
    RIGHT = 1
