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

    def set_cell_flag(self, row, col, flag):
        self.grid[row, col].cell_type = flag
        self.grid_as_ints[row, col] = flag
        if (flag == grid_cell_2d.VISITED_CELL):
            self.grid[row, col].mark_as_visted()

    def load_from_file(self, gridFile):
        grid = np.loadtxt(gridFile, dtype=int)
        self.num_rows = np.size(grid, 0)
        self.num_cols = np.size(grid, 1)
        self.__initialize_grid()
        for row in range(0, self.num_rows):
            for col in range(0, self.num_cols):
                self.grid[row, col] = grid_cell_2d.GridCell2D(row, col, grid[row, col])
                self.grid_as_ints[row, col] = grid[row, col]

                if self.grid_as_ints[row, col] == grid_cell_2d.START_CELL:
                    self.start_cell = self.grid[row, col]
                if self.grid_as_ints[row, col] == grid_cell_2d.GOAL_CELL:
                    self.goal_cell = self.grid[row, col]  
        
    def save_to_file(self, gridFile):
        np.savetxt(gridFile, self.grid_as_ints, fmt="%d")
    
    def save_grid_as_image(self, imageName):

        fig, ax = plt.subplots()
        ax.imshow(self.grid_as_ints, cmap=cmap, norm=norm)
        ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1)
        ax.set_xticks(np.arange(0.5, self.num_rows, 1));
        ax.set_yticks(np.arange(0.5, self.num_cols, 1));
        plt.tick_params(axis='both', which='both', bottom=False, left=False, labelbottom=False, labelleft=False)

        plt.savefig(imageName + ".png", dpi=500)
        plt.close()

    def set_start_cell(self, startRow, startCol):
        self.set_cell_flag(startRow, startCol, grid_cell_2d.START_CELL)
        self.start_cell = self.grid[startRow, startCol]

    def set_goal_cell(self, goalRow, goalCol):
        self.set_cell_flag(goalRow, goalCol, grid_cell_2d.GOAL_CELL)
        self.goal_cell = self.grid[goalRow, goalCol]  

    def add_obstacles(self, numberOfObstacles):

        for i in range(0, numberOfObstacles):
            col = random.randint(0, self.num_cols - 1)
            row = random.randint(0, self.num_rows - 1)
            # Only generate an obstacle if the cell is empty, aka
            # not the start, goal, or already an obstacle
            while self.grid_as_ints[row, col] != 0:
                col = random.randint(0, self.num_cols - 1)
                row = random.randint(0, self.num_rows - 1)

            self.set_cell_flag(row, col, grid_cell_2d.OBSTACLE_CELL)

    def __initialize_grid(self):
        self.grid = np.empty(self.num_rows * self.num_cols, dtype=grid_cell_2d.GridCell2D).reshape(self.num_rows, self.num_cols)
        self.grid_as_ints = np.zeros(self.num_rows * self.num_cols, dtype=int).reshape(self.num_rows, self.num_cols)
        for row in range(0, self.num_rows):
            for col in range(0, self.num_cols):
                self.grid[row, col] = grid_cell_2d.GridCell2D(row, col, grid_cell_2d.EMPTY_CELL)
                
if __name__ == "__main__":
    grid = Grid2D(20, 100)
    #grid.load_from_file('fixed_grid/fixed_grid.txt')
    print(grid.grid[19, 99].row)
    grid.set_cell_flag(19, 99, grid_cell_2d.GOAL_CELL)
    grid.save_grid_as_image("test")