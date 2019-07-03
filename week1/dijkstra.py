#!/usr/bin/env python

import numpy as np
from grid import *
import queue
from grid_waypoint import GridWayPoint

debug_file = open("images/dijkstra/dijkstra_debug.txt", "w+")

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
        # Flag the cell as the current cell. This is only needed for 
        # coloring/visualization
        grid[wp.x, wp.y] |= GridFlags.CURRENT
        debug_file.write("----------------------------------------------------\n")
        debug_file.write("Current Waypoint is: " + str(wp) + "\n")
        debug_file.write("Number of waypoints in queue: " + str(frontier.qsize()) + "\n")

        if (wp.x == grid.goal_waypoint.x and wp.y == grid.goal_waypoint.y):
            debug_file.write("Found goal, exiting loop")
            break
        neighbors = find_neighbors(wp, grid, allowDiagonalMoves)
        for neighbor in neighbors:
            # Need to accumulate the cost, so take the cost to get from the start
            # to the current waypoint, and the cost of moving from the current
            # waypoint to the neighbor
            new_cost = costs[wp] + abs(wp.x - neighbor.x) + abs(wp.y - neighbor.y)
            debug_file.write("~~~~~~~~~~~" + "\n")
            debug_file.write("Neighbor: " + str(wp) + "\n")
            debug_file.write("Cost calculated is: " + str(new_cost) + "\n")
            # We have a cost for this neighbor, but we need to do two checks:
            # 1. Is this a new neighbor? never been visited before?
            # 2. If it has been visited before, is the new cost lower
            # then the previous calculated cost. This would indicate we have found
            # a "better" path to this neighbor
            #
            # First check, this cell is never been visited, and the 
            # second check is checking that the new cost is lest the previously
            # calculated cost
            if neighbor not in costs or new_cost < costs[neighbor]:
                # Check only for debugging, if cost is lower write it to file
                if neighbor in costs and new_cost < costs[neighbor]:
                    debug_file.write("Lower cost determined, previous cost was: " + str(costs[neighbor]) + "\n")
                costs[neighbor] = new_cost
                # Update the parent cell as well
                parents[neighbor] = wp
                frontier.put(neighbor, new_cost)
                # Mark the cell as visited, this is just for visualization
                grid[neighbor.x, neighbor.y] |= GridFlags.VISITED

        # Turn off the current flag, only needed for visualization
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
            neighbors.append(wp)
    
    return neighbors

if __name__ == "__main__":


    grid = Grid(gridFile = "fixed_grid/new_fixed_grid.txt")
    dijkstra_solve(grid)
    grid.save_grid_as_image("images/dijkstra/dijkstra_4_moves")
    grid.load_from_file("fixed_grid/new_fixed_grid.txt")
    dijkstra_solve(grid, allowDiagonalMoves=True)
    grid.save_grid_as_image("images/dijkstra/dijkstra_8_moves")