#!/usr/bin/env python

import numpy as np
from grid import *
import queue
from grid_waypoint import GridWayPoint

debug_file = open("images/dijkstra/dijkstra_debug.txt", "w+")

def dijkstra_solve(grid, 
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
            # Greedy approach weights the distance to goal waypoint, closer the better
            new_cost = weightXDistance * abs(goal_wp.x - neighbor.x) + weightYDistance * abs(goal_wp.y - neighbor.y)
            if avoidObstacles:
                if grid.is_near_obstacle(neighbor, allowDiagonalMoves):
                    new_cost += 10000

            debug_file.write("~~~~~~~~~~~" + "\n")
            debug_file.write("Neighbor: " + str(neighbor) + "\n")
            debug_file.write("Cost calculated is: " + str(new_cost) + "\n")
            
            # If the waypoint has not been visited add it
            if not grid[neighbor.x, neighbor.y] & GridFlags.VISITED:
                frontier.put((new_cost, neighbor))
                # Mark the cell as visited
                grid[neighbor.x, neighbor.y] |= GridFlags.VISITED
                # Update the parent cell as well
                parents[neighbor] = wp

        # Turn off the current flag, only needed for visualization
        grid[wp.x, wp.y] &= ~GridFlags.CURRENT

    parent = parents[wp]
    number_of_steps = 1
    while parent is not None:
        grid[parent.x, parent.y] |= GridFlags.PATH
        parent = parents[parent]
        number_of_steps += 1
    print("Total number of steps: " + str(number_of_steps))
    return number_of_steps

if __name__ == "__main__":


    grid = Grid(gridFile = "fixed_grid/new_fixed_grid.txt")
    # Default behavior
    num_steps = dijkstra_solve(grid, 
        allowDiagonalMoves=False, 
        weightXDistance=1, 
        weightYDistance=1,
        avoidObstacles=False)
    grid.save_grid_as_image("images/dijkstra/dijkstra_4_moves_greedy",
        titleFigure = "4 Moves Equal weighting\n" + str(num_steps) + " Number of steps")
    # Weighting X direction
    grid.load_from_file("fixed_grid/new_fixed_grid.txt")
    num_steps = dijkstra_solve(grid, 
        allowDiagonalMoves=False, 
        weightXDistance=100, 
        weightYDistance=1,
        avoidObstacles=False)
    grid.save_grid_as_image("images/dijkstra/dijkstra_4_moves_greedy_xweighted",
        titleFigure = "4 Moves 100 X weighting\n" + str(num_steps) + " Number of steps")
    # Weighting Y direction
    grid.load_from_file("fixed_grid/new_fixed_grid.txt")
    num_steps = dijkstra_solve(grid, 
        allowDiagonalMoves=False, 
        weightXDistance=1, 
        weightYDistance=100,
        avoidObstacles=False)
    grid.save_grid_as_image("images/dijkstra/dijkstra_4_moves_greedy_yweighted",
        titleFigure = "4 Moves 100 Y weighting\n" + str(num_steps) + " Number of steps")
    # Avoid Obstacles
    grid.load_from_file("fixed_grid/new_fixed_grid.txt")
    num_steps = dijkstra_solve(grid, 
        allowDiagonalMoves=False, 
        weightXDistance=1, 
        weightYDistance=1,
        avoidObstacles=True)
    grid.save_grid_as_image("images/dijkstra/dijkstra_4_moves_greedy_avoid_obstacles",
        titleFigure = "4 Moves Equal weighting avoid obstalces\n" + str(num_steps) + " Number of steps")

    """ -------------------------------------
        Allowing Diagonal moves
        -------------------------------------
    """

    grid.load_from_file("fixed_grid/new_fixed_grid.txt")
    # Default behavior
    num_steps = dijkstra_solve(grid, 
        allowDiagonalMoves=True, 
        weightXDistance=1, 
        weightYDistance=1,
        avoidObstacles=False)
    grid.save_grid_as_image("images/dijkstra/dijkstra_8_moves_greedy",
        titleFigure = "8 Moves Equal weighting\n" + str(num_steps) + " Number of steps")
    # Weighting X direction
    grid.load_from_file("fixed_grid/new_fixed_grid.txt")
    num_steps = dijkstra_solve(grid, 
        allowDiagonalMoves=True, 
        weightXDistance=100, 
        weightYDistance=1,
        avoidObstacles=False)
    grid.save_grid_as_image("images/dijkstra/dijkstra_8_moves_greedy_xweighted",
        titleFigure = "8 Moves 100 X weighting\n" + str(num_steps) + " Number of steps")
    # Weighting Y direction
    grid.load_from_file("fixed_grid/new_fixed_grid.txt")
    num_steps = dijkstra_solve(grid, 
        allowDiagonalMoves=True, 
        weightXDistance=1, 
        weightYDistance=100,
        avoidObstacles=False)
    grid.save_grid_as_image("images/dijkstra/dijkstra_8_moves_greedy_yweighted",
        titleFigure = "8 Moves 100 Y weighting\n" + str(num_steps) + " Number of steps")
    # Avoid Obstacles
    grid.load_from_file("fixed_grid/new_fixed_grid.txt")
    num_steps = dijkstra_solve(grid, 
        allowDiagonalMoves=True, 
        weightXDistance=1, 
        weightYDistance=1,
        avoidObstacles=True)
    grid.save_grid_as_image("images/dijkstra/dijkstra_8_moves_greedy_avoid_obstacles",
        titleFigure = "8 Moves Equal weighting avoid obstalces\n" + str(num_steps) + " Number of steps")