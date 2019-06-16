import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

# BFS == Breadth First Search.
# This script plots the O notation (complexity) of using BFS
# to search a grid of N cells. In this example we are looking at 
# cells of 1, 2, 3, ... all the way to 1000 cells.
# And we are looking at the complexity up to 6 dimensions.
# So as a concrete example, what is the complexity to search a:
# 100x100 square
# 100x100x100 cube
# 100x100x100x100
# 100x100x100x100x100
# 100x100x100x100x100x100

number_of_cells_in_one_dimension = np.arange(101)
max_dimensions = 6
min_dimensions = 2
plt.figure()
# Need to offset range by 1 to include the max dimension
for num_dimension in range(min_dimensions, max_dimensions + 1):
    complexity = number_of_cells_in_one_dimension ** num_dimension
    # Create a label to display in the legend of the plot
    legend_label = str(num_dimension) + " Dimensions"
    plt.plot(number_of_cells_in_one_dimension, complexity, label=legend_label)
    
plt.legend()
plt.title("Breadth-First Search Complexity Zoomed Out")
plt.xlabel("Number of Cells in One Dimension")
plt.ylabel("Complexty O(|V|)")
plt.savefig("images/bfs_zoomed_out.png", dpi=500)

plt.title("Breadth-First Search Complexity Zoomed In")
plt.ylim([0, 1e6])
plt.ylabel("Complexty O(|V|)")
plt.savefig("images/bfs_zoomed_in.png", dpi=500)