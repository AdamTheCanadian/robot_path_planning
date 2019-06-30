#!/usr/bin/env python

""" Object for working with a single 2 dimensional grid cell
"""

from enum import Enum

EMPTY_CELL = 0
OBSTACLE_CELL = 1
START_CELL = 2
GOAL_CELL = 3
MOVE_CELL = 4
VISITED_CELL = 5
CURRENT_CELL = 6
PARENT_CELL = 7

class GridCell2D:

    def __init__(self, row = -1, col = -1, cellType = EMPTY_CELL):

        # The row/col location in the grid
        self.row = row
        self.col = col
        # Flag indicated the cell has been visited
        self.visited = False 
        # Parent cell. The parent cell is the cell that was visited
        # before this cell was visited
        self.parent_row = None
        self.parent_col = None
        # Flag to indicate what type of cell it is
        self.cell_type = cellType
    
    def mark_as_visted(self):
        self.visited = True

    def set_cell_flag(self, cellType):
        self.cell_type = cellType