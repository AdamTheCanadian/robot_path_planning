#!/usr/bin/env python

import numpy as np
from grid import *
import queue
from grid_waypoint import GridWayPoint

def dijkstra_solve(grid, allowDiagonalMoves=False):
    
    parents = {}
    costs = {}
    frontier = queue.PriorityQueue()
    start_wp = grid.start_waypoint
    # Add the start waypoint to the queue and mark it as visited
    frontier.put(start_wp, 0)
    parents[start_wp] = None
    grid[start_wp.x, start_wp.y] |= GridFlags.VISITED
    costs[start_wp] = 0

    wp = None
    while not frontier.empty():
        wp = frontier.get()
        print("Current wp: " + str(wp))
        # Flag the cell as the current cell. This is only needed for 
        # coloring/visualization
        grid[wp.x, wp.y] |= GridFlags.CURRENT

        if (wp.x == grid.goal_waypoint.x and wp.y == grid.goal_waypoint.y):
            print("Found goal")
            break
        neighbors = find_neighbors(wp, grid, allowDiagonalMoves)
        for neighbor in neighbors:
            cost = abs(start_wp.x - neighbor.x) + abs(start_wp.y - neighbor.y)
            frontier.put(neighbor, cost)
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
    dijkstra_solve(grid)
    grid.save_grid_as_image("dijkstra_4_moves")
    grid.load_from_file("fixed_grid/new_fixed_grid.txt")
    dijkstra_solve(grid, allowDiagonalMoves=True)
    grid.save_grid_as_image("dijkstra_8_moves")