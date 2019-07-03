#!/usr/bin/env python

""" Object for working with a single 2 dimensional grid
"""
import numpy as np
import random
import grid_waypoint
from enum import Enum
import matplotlib.pyplot as plt
from matplotlib import colors


class GridFlags:
    
    EMPTY = 0x00
    NEIGHBOR = 0x02
    VISITED = 0x04
    CURRENT = 0x08
    OBSTACLE = 0x10
    PATH = 0x20
    START = 0x40
    GOAL = 0x80

bounds = [
    GridFlags.EMPTY,
    GridFlags.NEIGHBOR,
    GridFlags.VISITED,
    GridFlags.CURRENT,
    GridFlags.OBSTACLE,
    GridFlags.PATH,
    GridFlags.START,
    GridFlags.GOAL,
]
bounds.append(bounds[-1] + 1)
# create discrete colormap
cmap = colors.ListedColormap([
    'white', # empty cell
    'blue', # neighbor cell
    'cyan', # visited cell
    'purple', # current cell
    'black', # obstacle cell
    'yellow', # path cell
    'green', # start cell
    'red', # goal cell,
    ])
norm = colors.BoundaryNorm(bounds, cmap.N)

class Grid:

    """ Object for representing a 2D grid for robot path planning

    Internally the object uses a numpy 2D array. A numpy array is typically
    referenced by array[row, col], and the origin (0,0) is the top left of
    the array. Additionally this means the array is indexed by the [y, x] 
    value, not [x, y].

    For robot path planning, it is more intuitive to have the origin (0, 0)
    at the bottom left, so positive x is right direction, and positive y is 
    up direction, and secondly to have the array indexed by x/y value, not y/x.

    As such, there is some flipping of the values internally, and it is 
    recommended to use the overload access operators [x,y].

    Lastly, the grid internally is a set of flags that indicate the status of the
    grid cell. This was done as a cell can be in several states at once. For example
    a start cell, a visited cell, and a neighbor cell. 

    To set a flag to visited for example:
    grid[x, y] |= GridFlags.VISITED

    To query or test a flag if its an obstacle
    grid[x, y] & GridFlags.OBSTACLE
    """

    def __init__(self, sizeX = 1, sizeY = 1, gridFile = None):
        
        self.size_x = sizeX
        self.size_y = sizeY
        self.grid = np.zeros((self.size_y, self.size_x), dtype=int)
        # Keep a record of the start and goal waypoints, they are likely
        # to be used often
        self.start_waypoint = grid_waypoint.GridWayPoint()
        self.goal_waypoint = grid_waypoint.GridWayPoint()
        if gridFile is not None:
            self.load_from_file(gridFile)
        
    def load_from_file(self, gridFile):
        self.grid = np.loadtxt(gridFile, dtype=int)
        self.size_x = np.size(self.grid, 1)
        self.size_y = np.size(self.grid, 0)
        start = np.where(self.grid & GridFlags.START)
        if np.size(start, 1) > 0:
            self.start_waypoint.x = start[1][0]
            self.start_waypoint.y = start[0][0]
            print("Found starting waypoint: " + str(self.start_waypoint))
        goal = np.where(self.grid & GridFlags.GOAL)
        if np.size(goal, 1) > 0:
            self.goal_waypoint.x = goal[1][0]
            self.goal_waypoint.y = goal[0][0]
            print("Found goal waypoint: " + str(self.goal_waypoint))
    
    def set_start_waypoint(self, startX = 0, startY = 0, randomStart=False):
        if randomStart:
            startX = random.randint(0, self.size_x - 1)
            startY = random.randint(0, self.size_y - 1)

        self.grid[startY, startX] = GridFlags.START
        self.start_waypoint.x = startX
        self.start_waypoint.y = startY

    def set_goal_waypoint(self, goalX = 0, goalY = 0, randomGoal=False):
        if randomGoal:
            goalX = random.randint(0, self.size_x - 1)
            goalY = random.randint(0, self.size_y - 1)
            # Want to make sure the goal position that was randomly generated
            # is not the start position, so keep randomly getting positions
            # until its not the start anymore
            while self.grid[goalX, goalY] == GridFlags.START:
                goalX = random.randint(0, self.size_x - 1)
                goalY = random.randint(0, self.size_y - 1)

        self.grid[goalY, goalX] = GridFlags.GOAL
        self.goal_waypoint.x = goalX
        self.goal_waypoint.y = goalY

    def add_obstacles(self, numberOfObstacles):

        for i in range(0, numberOfObstacles):
            x = random.randint(0, self.size_x - 1)
            y = random.randint(0, self.size_y - 1)
            # Only generate an obstacle if the cell is empty, aka
            # not the start, goal, or already an obstacle
            while self.grid[y, x] & GridFlags.START or self.grid[y, x] & GridFlags.GOAL:
                x = random.randint(0, self.size_x - 1)
                y = random.randint(0, self.size_y - 1)

            self.grid[y, x] |= GridFlags.OBSTACLE

    def save_grid_to_file(self, gridFile):
        np.savetxt(gridFile, self.grid, fmt="%d")

    def save_grid_as_image(self, gridImageName):
        
        plt.imshow(self.grid, cmap=cmap, norm=norm, origin="lower")
        ax = plt.gca()
        # ax.set_xticks(np.arange(0.5, self.size_x, 1));
        # ax.set_yticks(np.arange(0.5, self.size_y, 1));
        # plt.tick_params(axis='both', which='both', bottom=False, left=False, labelbottom=False, labelleft=False)
        plt.savefig(gridImageName + ".png", dpi=500)
        plt.close()

    def is_waypoint_valid(self, waypoint):

        if waypoint.x < 0 or waypoint.x >= self.size_x:
            return False
        if waypoint.y < 0 or waypoint.y >= self.size_y:
            return False
        if self.grid[waypoint.y, waypoint.x] & GridFlags.OBSTACLE:
            return False
        
        return True

    def __getitem__(self, index):
        return self.grid[index[1], index[0]]
    
    def __setitem__(self, index, gridFlags):
        self.grid[index[1], index[0]] = gridFlags

if __name__ == "__main__":
    grid = Grid(100, 100)
    grid.set_goal_waypoint(95, 90)
    grid.set_start_waypoint(15, 5)
    grid.add_obstacles(1000)
    grid.save_grid_as_image("fixed_grid/new_fixed_grid_")
    grid.save_grid_to_file("fixed_grid/new_fixed_grid_.txt")
    grid.load_from_file("fixed_grid/new_fixed_grid_.txt")
    grid.save_grid_as_image("fixed_grid/new_fixed_grid2")