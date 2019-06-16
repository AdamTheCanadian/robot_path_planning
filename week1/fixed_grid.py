import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import random
import grid_generator

if __name__ == "__main__":

    data = grid_generator.generate_grid(10, 10)
    data[1, 1] = grid_generator.START_CELL
    data[9, 9] = grid_generator.GOAL_CELL
    grid_generator.generate_obstacles(data, 5)
    grid_generator.plot_grid(data, "fixed_grid/fixed_grid")
    # This line was puroposely commented out so I dont accidently 
    # overwrite my truth file. Uncomment if wanting to generate new
    # truth grid
    # np.savetxt("fixed_grid/fixed_grid.txt", data, fmt="%d")
