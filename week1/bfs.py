import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import random
import grid_generator
import queue

def move_8_directions():
    row_direction_vector = np.array([-1, 1, 0, 0, -1, -1, 1, 1])
    col_direction_vector = np.array([0, 0, 1, -1, -1, 1, 1, -1])

def move_4_directions(grid, currentRow, currentCol, rowQueue, colQueue):

    row_direction_vector = np.array([-1, 1, 0, 0])
    col_direction_vector = np.array([0, 0, 1, -1])

    row_moves = np.empty((0, 1), int)
    col_moves = np.empty((0, 1), int)
    
    num_rows = np.size(grid, 0)
    num_cols = np.size(grid, 1)
    
    for i in range(0, 4):
        new_row = currentRow + row_direction_vector[i]
        new_col = currentCol + col_direction_vector[i]
        if new_row < 0 or new_col < 0:
            continue
        if new_row >= num_rows or new_col >= num_cols:
            continue

        if grid[new_row, new_col] == grid_generator.VISITED_CELL:
            continue
        if grid[new_row, new_col] == grid_generator.OBSTACLE_CELL:
            continue
        rowQueue.put(new_row)
        colQueue.put(new_col)
        grid[new_row, new_col] = grid_generator.VISITED_CELL

def bfs_solve(grid):
    number_of_rows = np.size(grid, 0)
    number_of_cols = np.size(grid, 1)
    # Find the XY coordinate of the start
    start = np.where(grid == grid_generator.START_CELL)
    start_row = start[0]
    start_col = start[1]
    # How many steps/moves did the search take
    number_of_steps_taken = 0

    row_queue = queue.Queue()
    col_queue = queue.Queue()

    row_queue.put(start_row)
    col_queue.put(start_col)
    i = 0
    # Make sure this cell is labeled as visited
    grid[start_row, start_col] = grid_generator.VISITED_CELL
    while not row_queue.empty():
        row = row_queue.get()
        col = col_queue.get()
        if (grid[row, col] == grid_generator.GOAL_CELL):
            break
        move_4_directions(grid, row, col, row_queue, col_queue)
        grid_generator.plot_grid(grid, 'bfs_images/bfs_'+str(i))
        i = i + 1

if __name__ == "__main__":
    grid = np.loadtxt('fixed_grid/fixed_grid.txt', dtype=int)
    bfs_solve(grid)