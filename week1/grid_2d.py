#!/usr/bin/env python

""" Object for working with a single 2 dimensional grid
"""
import numpy as np
import random
import grid_cell_2d
import matplotlib.pyplot as plt
from matplotlib import colors

bounds = [grid_cell_2d.EMPTY_CELL, 
    grid_cell_2d.OBSTACLE_CELL, 
    grid_cell_2d.START_CELL, 
    grid_cell_2d.GOAL_CELL, 
    grid_cell_2d.MOVE_CELL, 
    grid_cell_2d.VISITED_CELL, 
    grid_cell_2d.CURRENT_CELL,
    grid_cell_2d.PARENT_CELL,
    grid_cell_2d.PARENT_CELL + 1]

# create discrete colormap
cmap = colors.ListedColormap([
    'white', # empty cell
    'black', # obstacle cell
    'green', # start cell
    'red', # goal cell
    'blue', # move cell
    'cyan', # visited cell
    'purple', # current cell
    'yellow', # parent cell
    ])
norm = colors.BoundaryNorm(bounds, cmap.N)


class Grid2D:

    def __init__(self, numRows = 1, numCols = 1):
        
        self.num_rows = numRows
        self.num_cols = numCols
        self.__initialize_grid()
        # Keep a record of the start and goal cell as these will
        # likely be looked up frequently
        self.start_cell = grid_cell_2d.GridCell2D()
        self.goal_cell = grid_cell_2d.GridCell2D()

    def set_cell_flag(self, x, y, flag):
        self.grid[x, y].cell_type = flag
        self.grid_as_ints[x, y] = flag
        if (flag == grid_cell_2d.VISITED_CELL):
            self.grid[x, y].mark_as_visted()

    def load_from_file(self, gridFile):
        grid = np.loadtxt(gridFile, dtype=int)
        self.num_rows = np.size(grid, 0)
        self.num_cols = np.size(grid, 1)
        self.__initialize_grid()
        for x in range(0, self.num_rows):
            for y in range(0, self.num_cols):
                self.grid[x, y] = grid_cell_2d.GridCell2D(x, y, grid[x, y])
                self.grid_as_ints[x, y] = grid[x, y]

                if self.grid_as_ints[x, y] == grid_cell_2d.START_CELL:
                    self.start_cell = self.grid[x, y]
                if self.grid_as_ints[x, y] == grid_cell_2d.GOAL_CELL:
                    self.goal_cell = self.grid[x, y]
    
    def save_to_file(self, gridFile):
        pass
    
    def save_grid_as_image(self, imageName):

        fig, ax = plt.subplots()
        ax.imshow(self.grid_as_ints, cmap=cmap, norm=norm)
        ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1)
        ax.set_xticks(np.arange(0.5, self.num_rows, 1));
        ax.set_yticks(np.arange(0.5, self.num_cols, 1));
        plt.tick_params(axis='both', which='both', bottom=False, left=False, labelbottom=False, labelleft=False)

        plt.savefig(imageName + ".png", dpi=500)
        plt.close()

    def __initialize_grid(self):
        self.grid = np.empty(self.num_rows * self.num_cols, dtype=grid_cell_2d.GridCell2D).reshape(self.num_rows, self.num_cols)
        self.grid_as_ints = np.zeros(self.num_rows * self.num_cols, dtype=int).reshape(self.num_rows, self.num_cols)
       
    def __grid_to_int(self):
        for x in range(0, self.num_rows):
            for y in range(0, self.num_cols):
                self.grid_as_ints[x , y] = self.grid[x, y].cell_type

if __name__ == "__main__":
    grid = Grid2D()
    grid.load_from_file('fixed_grid/fixed_grid.txt')
    grid.save_grid_as_image('test')