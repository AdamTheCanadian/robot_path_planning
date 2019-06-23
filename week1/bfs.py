import numpy as np
import grid_tools
import queue

# Global count that is incremented every time an image is saved
image_number = 0
# Global grid, only made global to avoid passing in every function
grid = None
# Array to keep a record if the cell was visited
visted_flags = None
number_of_rows = 0
number_of_cols = 0
# Index of where the start position is
start_row = -1
start_col = -1
# Index of where the goal position is
goal_row = -1
goal_col = -1
# For holding the cells that need to be checked
row_queue = queue.Queue()
col_queue = queue.Queue()

def move_8_directions():
    row_direction_vector = np.array([-1, 1, 0, 0, -1, -1, 1, 1])
    col_direction_vector = np.array([0, 0, 1, -1, -1, 1, 1, -1])

def move_4_directions(currentRow, currentCol):

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

        if visted_flags[new_row, new_col] == grid_tools.VISITED_CELL:
            continue
        if grid[new_row, new_col] == grid_tools.OBSTACLE_CELL:
            continue
        row_queue.put(new_row)
        col_queue.put(new_col)
        grid[new_row, new_col] = grid_tools.VISITED_CELL
        bfs_save_grid()
        visted_flags[new_row, new_col] = grid_tools.VISITED_CELL

def bfs_solve():

    find_start_position()
    find_goal_position()
    global start_row
    global start_col
    global goal_row
    global goal_col
    global image_number
    global grid
    # How many steps/moves did the search take
    number_of_steps_taken = 0
    row_queue.put(start_row)
    col_queue.put(start_col)
    # Make sure this cell is labeled as visited
    visted_flags[start_row, start_col] = grid_tools.VISITED_CELL
    while not row_queue.empty():
        row = row_queue.get()
        col = col_queue.get()
        print("Image number: " + str(image_number))
        print("Current cell: " + str(row) + ", " + str(col))
        if (row == goal_row and col == goal_col):
            break
        # If the current cell is not the start cell change the flag 
        # to change the color when plotting. The reason for not 
        # changing it when the start position is just to keep the
        # color of the start cell consistent across images
        if row != start_row or col != start_col:
            grid[row, col] = grid_tools.CURRENT_CELL
        bfs_save_grid()
        move_4_directions(row, col)
        # Change the color back
        if (row != start_row or col != start_col):
            grid[row, col] = grid_tools.VISITED_CELL

def bfs_save_grid():
    global image_number
    grid_tools.save_grid(grid, 'bfs_images/bfs_'+str(image_number))
    image_number = image_number + 1

def find_start_position():
    global start_row
    global start_col
    # Find the XY coordinate of the start
    start = np.where(grid == grid_tools.START_CELL)
    start_row = start[0]
    start_col = start[1]
    if (start_row >= 0 and start_col >=0):
        print("Found starting position at " + str(start_row) + ", " + str(start_col))

def find_goal_position():
    global goal_row
    global goal_col
    # Find the XY coordinate of the goal
    goal = np.where(grid == grid_tools.GOAL_CELL)
    goal_row = goal[0]
    goal_col = goal[1]
    if (goal_row >= 0 and goal_col >=0):
        print("Found goal position at " + str(goal_row) + ", " + str(goal_col))

if __name__ == "__main__":
    grid = np.loadtxt('fixed_grid/fixed_grid.txt', dtype=int)
    number_of_rows = np.size(grid, 0)
    number_of_cols = np.size(grid, 1)
    visted_flags = grid_tools.generate_grid(number_of_rows, number_of_cols)
    bfs_solve()