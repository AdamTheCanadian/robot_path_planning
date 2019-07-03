#!/usr/bin/env python

import numpy as np
from grid import *
import queue
from grid_waypoint import GridWayPoint

def bfs_solve(grid, allowDiagonalMoves=False):
    
    parents = {}
    frontier = queue.Queue()
    # Add the start waypoint to the queue and mark it as visited
    frontier.put(grid.start_waypoint)
    parents[grid.start_waypoint] = None
    grid[grid.start_waypoint.x, grid.start_waypoint.y] |= GridFlags.VISITED
    
    wp = None
    while not frontier.empty():
        wp = frontier.get()
        # Flag the cell as the current cell. This is only needed for 
        # coloring/visualization
        grid[wp.x, wp.y] |= GridFlags.CURRENT

        if (wp.x == grid.goal_waypoint.x and wp.y == grid.goal_waypoint.y):
            print("Found goal")
            break
        neighbors = find_neighbors(wp, grid, allowDiagonalMoves)
        for neighbor in neighbors:
            frontier.put(neighbor)
            parents[neighbor] = wp
        
        # Turn off the current flag
        grid[wp.x, wp.y] &= ~GridFlags.CURRENT

    parent = parents[wp]
    number_of_steps = 1
    while parent is not None:
        grid[parent.x, parent.y] |= GridFlags.PATH
        parent = parents[parent]
        number_of_steps += 1

def find_neighbors(waypoint, grid, allowDiagonalMoves):
    
    x_directions = [-1, 1, 0, 0]
    y_directions = [0, 0, 1, -1]
    
    if allowDiagonalMoves:
        x_directions = [-1, 1, 0, 0, -1, -1, 1, 1]
        y_directions = [0, 0, 1, -1, -1, 1, 1, -1]
        
    neighbors = []
    for i in range(0, len(x_directions)):
        wp = GridWayPoint(
            waypoint.x + x_directions[i],
            waypoint.y + y_directions[i])

        if grid.is_waypoint_valid(wp):
            if grid[wp.x, wp.y] & GridFlags.VISITED:
                continue
            neighbors.append(wp)
            grid[wp.x, wp.y] |= GridFlags.VISITED
    
    return neighbors

if __name__ == "__main__":

    grid = Grid(gridFile = "fixed_grid/new_fixed_grid.txt")
    bfs_solve(grid)
    grid.save_grid_as_image("images/bfs/bfs_4_moves")