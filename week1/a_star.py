#!/usr/bin/env python
import numpy as np
from grid import *
import queue
from grid_waypoint import GridWayPoint

debug_file = open("images/astar/astar_debug.txt", "w+")


def astar_solve(grid, 
    allowDiagonalMoves = False,
    avoidObstacles = False,
    weightXDistance = 1,
    weightYDistance = 1):
    
    parents = {}
    costs = {}
    frontier = queue.PriorityQueue()

    start_wp = grid.start_waypoint
    goal_wp = grid.goal_waypoint
    # Add the start waypoint to the queue and mark it as visited
    frontier.put((0, start_wp))
    parents[start_wp] = None
    grid[start_wp.x, start_wp.y] |= GridFlags.VISITED
    costs[start_wp] = 0

    wp = None
    while not frontier.empty():
        wp = frontier.get()[1]
        # Flag the cell as the current cell. This is only needed for 
        # coloring/visualization
        grid[wp.x, wp.y] |= GridFlags.CURRENT
        debug_file.write("----------------------------------------------------\n")
        debug_file.write("Current Waypoint is: " + str(wp) + "\n")
        debug_file.write("Number of waypoints in queue: " + str(frontier.qsize()) + "\n")
        
        if (wp.x == grid.goal_waypoint.x and wp.y == grid.goal_waypoint.y):
            debug_file.write("Found goal, exiting loop")
            break
        neighbors = grid.find_neighbors(wp, allowDiagonalMoves)
        for neighbor in neighbors:
            # Need to accumulate the cost, so take the cost to get from the start
            # to the current waypoint, and the cost of moving from the current
            # waypoint to the neighbor
            new_cost = costs[wp] + weightXDistance * abs(wp.x - neighbor.x) + weightYDistance * abs(wp.y - neighbor.y)
                        
            if avoidObstacles:
                if grid.is_near_obstacle(neighbor, allowDiagonalMoves):
                    new_cost += 10000

            debug_file.write("~~~~~~~~~~~" + "\n")
            debug_file.write("Neighbor: " + str(neighbor) + "\n")
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
                
                cost_to_goal = weightXDistance * abs(goal_wp.x - neighbor.x) + weightYDistance * abs(goal_wp.y - neighbor.y)
                costs[neighbor] = new_cost
                # Update the parent cell as well
                parents[neighbor] = wp
                frontier.put((new_cost + cost_to_goal, neighbor))
                # Mark the cell as visited, this is just for visualization
                grid[neighbor.x, neighbor.y] |= GridFlags.VISITED

        # Turn off the current flag, only needed for visualization
        grid[wp.x, wp.y] &= ~GridFlags.CURRENT

    parent = parents[wp]
    number_of_steps = 1
    total_cost = costs[wp]
    while parent is not None:
        grid[parent.x, parent.y] |= GridFlags.PATH
        parent = parents[parent]
        number_of_steps += 1
        total_cost += costs[wp]
    print("Total number of steps: " + str(number_of_steps))
    print("Total cost: " + str(total_cost))
    return number_of_steps

if __name__ == "__main__":
    grid = Grid(gridFile = "fixed_grid/new_fixed_grid.txt")

    num_steps = astar_solve(grid,allowDiagonalMoves=True,  avoidObstacles=False)
    grid.save_grid_as_image("images/astar/astar_8_moves",
        titleFigure = "8 Moves Equal weighting\n" + str(num_steps) + " Number of steps")
            
    grid.load_from_file("fixed_grid/new_fixed_grid.txt")
    num_steps = astar_solve(grid, 
        allowDiagonalMoves=True, 
        weightXDistance=1, 
        weightYDistance=1,
        avoidObstacles=True)
    grid.save_grid_as_image("images/astar/astar_8_moves_avoid_obstacles",
        titleFigure = "8 Moves Equal weighting\n" + str(num_steps) + " Number of steps")
    