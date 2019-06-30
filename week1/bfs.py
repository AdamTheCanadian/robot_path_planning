import numpy as np
import grid_tools
import queue

import grid_2d
import grid_cell_2d
# For holding the cells that need to be checked
cell_queue = queue.Queue()

image_count = 0

def move_8_directions(grid, currentCell):
    global image_count
    y_direction_vector = np.array([-1, 1, 0, 0, -1, -1, 1, 1])
    x_direction_vector = np.array([0, 0, 1, -1, -1, 1, 1, -1])
    for i in range(0, 8):
        new_x = currentCell.x + x_direction_vector[i]
        new_y = currentCell.y + y_direction_vector[i]
        if new_x < 0 or new_y < 0:
            continue
        if new_x >= grid.num_cols or new_y >= grid.num_rows:
            continue

        if grid.grid[new_x, new_y].visited:
            continue
        if grid.grid[new_x, new_y].cell_type == grid_cell_2d.OBSTACLE_CELL:
            continue
        cell_queue.put(grid.grid[new_x, new_y])
        # Set the parents of the cell
        grid.grid[new_x, new_y].parent_x = currentCell.x
        grid.grid[new_x, new_y].parent_y = currentCell.y
        grid.set_cell_flag(new_x, new_y, grid_cell_2d.MOVE_CELL)
        # Going to color the parent cell before saving, and then change it back
        previous_type = grid.grid[currentCell.x, currentCell.y].cell_type
        grid.set_cell_flag(currentCell.x, currentCell.y, grid_cell_2d.PARENT_CELL)
        grid.save_grid_as_image("bfs_images/bfs_8_move_fixed_grid/bfs_" + str(image_count))
        image_count += 1
        grid.set_cell_flag(currentCell.x, currentCell.y, previous_type)
        grid.set_cell_flag(new_x, new_y, grid_cell_2d.VISITED_CELL)

def move_4_directions(grid, currentCell):

    global image_count
    y_direction_vector = np.array([-1, 1, 0, 0])
    x_direction_vector = np.array([0, 0, 1, -1])

    for i in range(0, 4):
        new_x = currentCell.x + x_direction_vector[i]
        new_y = currentCell.y + y_direction_vector[i]
        if new_x < 0 or new_y < 0:
            continue
        if new_x >= grid.num_cols or new_y >= grid.num_rows:
            continue

        if grid.grid[new_x, new_y].visited:
            continue
        if grid.grid[new_x, new_y].cell_type == grid_cell_2d.OBSTACLE_CELL:
            continue
        cell_queue.put(grid.grid[new_x, new_y])
        # Set the parents of the cell
        grid.grid[new_x, new_y].parent_x = currentCell.x
        grid.grid[new_x, new_y].parent_y = currentCell.y
        grid.set_cell_flag(new_x, new_y, grid_cell_2d.MOVE_CELL)
        # Going to color the parent cell before saving, and then change it back
        previous_type = grid.grid[currentCell.x, currentCell.y].cell_type
        grid.set_cell_flag(currentCell.x, currentCell.y, grid_cell_2d.PARENT_CELL)
        grid.save_grid_as_image("bfs_images/bfs_" + str(image_count))
        image_count += 1
        grid.set_cell_flag(currentCell.x, currentCell.y, previous_type)
        grid.set_cell_flag(new_x, new_y, grid_cell_2d.VISITED_CELL)

def bfs_solve(grid):

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
            grid.set_cell_flag(cell.x, cell.y, grid_cell_2d.CURRENT_CELL)

        grid.save_grid_as_image("bfs_images/bfs_8_move_fixed_grid/bfs_" + str(image_count))
        image_count += 1
        move_8_directions(grid, cell)
        # Change the color back
        if cell != grid.start_cell:
            grid.set_cell_flag(cell.x, cell.y, grid_cell_2d.VISITED_CELL)

    if goal_cell != None:
        current_cell = goal_cell
        while current_cell.parent_x is not None:
            grid.set_cell_flag(current_cell.parent_x, current_cell.parent_y, grid_cell_2d.MOVE_CELL)
            current_cell = grid.grid[current_cell.parent_x, current_cell.parent_y]

    # Update the goal cell and start cell flags so the colors change in
    # the final output
    grid.set_cell_flag(grid.start_cell.x, grid.start_cell.y, grid_cell_2d.START_CELL)
    grid.set_cell_flag(grid.goal_cell.x, grid.goal_cell.y, grid_cell_2d.GOAL_CELL)
    grid.save_grid_as_image("bfs_images/bfs_8_move_fixed_grid/bfs_final")

if __name__ == "__main__":
    grid = grid_2d.Grid2D()
    grid.load_from_file('fixed_grid/fixed_grid.txt')
    bfs_solve(grid)