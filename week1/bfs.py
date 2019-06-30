import numpy as np
import queue

import grid_2d
import grid_cell_2d
# For holding the cells that need to be checked
cell_queue = queue.Queue()

image_count = 0
image_path = "bfs_images/bfs_4_move_large_grid_100/"

def move_8_directions(grid, currentCell):
    global image_count
    row_direction_vector = np.array([-1, 1, 0, 0, -1, -1, 1, 1])
    col_direction_vector = np.array([0, 0, 1, -1, -1, 1, 1, -1])
    for i in range(0, 8):
        new_col = currentCell.row + col_direction_vector[i]
        new_row = currentCell.col + row_direction_vector[i]
        if new_col < 0 or new_row < 0:
            continue
        if new_col >= grid.num_cols or new_row >= grid.num_rows:
            continue

        if grid.grid[new_col, new_row].visited:
            continue
        if grid.grid[new_col, new_row].cell_type == grid_cell_2d.OBSTACLE_CELL:
            continue
        cell_queue.put(grid.grid[new_col, new_row])
        # Set the parents of the cell
        grid.grid[new_col, new_row].parent_row = currentCell.row
        grid.grid[new_col, new_row].parent_col = currentCell.col
        grid.set_cell_flag(new_col, new_row, grid_cell_2d.MOVE_CELL)
        # Going to color the parent cell before saving, and then change it back
        previous_type = grid.grid[currentCell.row, currentCell.col].cell_type
        grid.set_cell_flag(currentCell.row, currentCell.col, grid_cell_2d.PARENT_CELL)
        bfs_save(grid)
        grid.set_cell_flag(currentCell.row, currentCell.col, previous_type)
        grid.set_cell_flag(new_col, new_row, grid_cell_2d.VISITED_CELL)

def move_4_directions(grid, currentCell):

    global image_count
    row_direction_vector = np.array([-1, 1, 0, 0])
    col_direction_vector = np.array([0, 0, 1, -1])

    for i in range(0, 4):
        new_col = currentCell.row + col_direction_vector[i]
        new_row = currentCell.col + row_direction_vector[i]
        if new_col < 0 or new_row < 0:
            continue
        if new_col >= grid.num_cols or new_row >= grid.num_rows:
            continue

        if grid.grid[new_col, new_row].visited:
            continue
        if grid.grid[new_col, new_row].cell_type == grid_cell_2d.OBSTACLE_CELL:
            continue
        cell_queue.put(grid.grid[new_col, new_row])
        # Set the parents of the cell
        grid.grid[new_col, new_row].parent_row = currentCell.row
        grid.grid[new_col, new_row].parent_col = currentCell.col
        grid.set_cell_flag(new_col, new_row, grid_cell_2d.MOVE_CELL)
        # Going to color the parent cell before saving, and then change it back
        previous_type = grid.grid[currentCell.row, currentCell.col].cell_type
        grid.set_cell_flag(currentCell.row, currentCell.col, grid_cell_2d.PARENT_CELL)
        bfs_save(grid)
        grid.set_cell_flag(currentCell.row, currentCell.col, previous_type)
        grid.set_cell_flag(new_col, new_row, grid_cell_2d.VISITED_CELL)

def bfs_solve(grid, use8Move):

    goal_cell = None
    global image_count
    # How many steps/moves did the search take
    number_of_steps_taken = 0
    cell_queue.put(grid.start_cell)
    # Make sure to set the cell as visited
    grid.start_cell.mark_as_visted()

    while not cell_queue.empty():
        cell = cell_queue.get()
        if (cell == grid.goal_cell):
            goal_cell = cell
            break
        # If the current cell is not the start cell change the flag 
        # to change the color when plotting. The reason for not 
        # changing it when the start position is just to keep the
        # color of the start cell consistent across images
        if cell != grid.start_cell:
            grid.set_cell_flag(cell.row, cell.col, grid_cell_2d.CURRENT_CELL)

        bfs_save(grid)
        if use8Move:
            move_8_directions(grid, cell)
        else:
            move_4_directions(grid, cell)
        # Change the color back
        if cell != grid.start_cell:
            grid.set_cell_flag(cell.row, cell.col, grid_cell_2d.VISITED_CELL)

    if goal_cell != None:
        current_cell = goal_cell
        while current_cell.parent_row is not None:
            grid.set_cell_flag(current_cell.parent_row, current_cell.parent_col, grid_cell_2d.MOVE_CELL)
            bfs_save(grid)
            current_cell = grid.grid[current_cell.parent_row, current_cell.parent_col]

    # Update the goal cell and start cell flags so the colors change in
    # the final output
    grid.set_cell_flag(grid.start_cell.row, grid.start_cell.col, grid_cell_2d.START_CELL)
    grid.set_cell_flag(grid.goal_cell.row, grid.goal_cell.col, grid_cell_2d.GOAL_CELL)
    bfs_save(grid)

def bfs_save(grid):
    global image_count
    global image_path
    grid.save_grid_as_image(image_path + "bfs_" + str(image_count))
    image_count += 1

if __name__ == "__main__":
    grid = grid_2d.Grid2D(25, 25)
    # grid.set_start_cell(15, 18)
    # grid.set_goal_cell(19, 3)
    # grid.add_obstacles(100)
    # print(grid.goal_cell.row)
    # grid.save_to_file("fixed_grid/large_grid.txt")
    grid.load_from_file("fixed_grid/fixed_grid.txt")
    use_8_move = False
    bfs_solve(grid, use_8_move)