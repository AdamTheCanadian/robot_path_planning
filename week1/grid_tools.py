import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import random

EMPTY_CELL = 0
OBSTACLE_CELL = 1
START_CELL = 2
GOAL_CELL = 3
MOVE_CELL = 4
VISITED_CELL = 5
CURRENT_CELL = 6
direction_row = np.array([-1, 1, 0, 0])
direction_col = np.array([0, 0, 1, -1])
# create discrete colormap
cmap = colors.ListedColormap(['white', 'black', 'green', 'red', 'blue', 'cyan', 'purple'])
bounds = [EMPTY_CELL, 
    OBSTACLE_CELL, 
    START_CELL, 
    GOAL_CELL, 
    MOVE_CELL, 
    VISITED_CELL, 
    CURRENT_CELL,
    CURRENT_CELL + 1]
norm = colors.BoundaryNorm(bounds, cmap.N)

def show_grid(grid):
    num_rows = np.size(grid, 0)
    num_cols = np.size(grid, 1)
    fig, ax = plt.subplots()
    ax.imshow(grid, cmap=cmap, norm=norm)
    # draw gridlines
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1)
    ax.set_xticks(np.arange(0.5, num_rows, 1));
    ax.set_yticks(np.arange(0.5, num_cols, 1));
    plt.tick_params(axis='both', which='both', bottom=False, left=False, labelbottom=False, labelleft=False)
    plt.show()

def save_grid(data, saveImageName):

    num_rows = np.size(data, 0)
    num_cols = np.size(data, 1)
    fig, ax = plt.subplots()
    ax.imshow(data, cmap=cmap, norm=norm)
    # draw gridlines
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1)
    ax.set_xticks(np.arange(0.5, num_rows, 1));
    ax.set_yticks(np.arange(0.5, num_cols, 1));
    plt.tick_params(axis='both', which='both', bottom=False, left=False, labelbottom=False, labelleft=False)
    # fig.set_size_inches((8.5, 11), forward=False)
    plt.savefig(saveImageName + ".png", dpi=500)
    plt.close()

def generate_moves(grid, startX, startY):
    num_rows = np.size(grid, 0)
    num_cols = np.size(grid, 1)

    # Theres only 4 possible moves, up down left right
    for i in range(0, 4):

        new_x = startX + direction_row[i]
        new_y = startY + direction_col[i]

        if new_x < 0 or new_y < 0:
            continue
        if new_x >= num_rows or new_y >= num_cols:
            continue
        if grid[new_x, new_y] == 0:
            grid[new_x, new_y] = MOVE_CELL

def generate_grid(rows, columns):
    return np.zeros(rows * columns, dtype=int).reshape(rows, columns)

def generate_obstacles(grid, numberOfObstacles):

    num_rows = np.size(grid, 0)
    num_cols = np.size(grid, 1)
    for i in range(0, numberOfObstacles):
        x = random.randint(0, num_rows - 1)
        y = random.randint(0, num_cols - 1)
        while grid[x, y] != 0:
            x = random.randint(0, num_rows - 1)
            y = random.randint(0, num_cols - 1)

        grid[x, y] = OBSTACLE_CELL

if __name__ == "__main__":
    rows = 20
    cols = 20
    # Randomly create 20 different grids
    for i in range(0, 20):

        data = generate_grid(rows, cols)
        start_x = random.randint(0, rows - 1)
        start_y = random.randint(0, cols - 1)
        data[start_x, start_y] = START_CELL
        
        goal_x = random.randint(0, rows - 1)
        # Dont want the start and end positions to be the same
        # so keep changing the goal x until its different. 
        # If X is different dont need to check Y
        while goal_x is start_x:
            goal_x = random.randint(0, rows - 1)
        goal_y = random.randint(0, cols - 1)

        data[goal_x, goal_y] = GOAL_CELL
        generate_obstacles(data, 10)
        generate_moves(data, start_x, start_y)
        save_grid(data, "week1/images/grid_" + str(i))