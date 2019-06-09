import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

rows = 10
cols = 10
data = np.zeros(rows * cols).reshape(rows, cols)
# Hard coding the start, goal, and obstacles for now.
data[1, 1] = 2
data[9, 9] = 3
data[4, 4] = 1
data[5, 5] = 1
# Possible moves
data[0, 1] = 5
data[1, 0] = 5
data[1, 2] = 5
data[2, 1] = 5
# create discrete colormap
cmap = colors.ListedColormap(['white', 'black', 'green', 'red', 'blue'])
bounds = [0,1,2,3,4,5]
norm = colors.BoundaryNorm(bounds, cmap.N)

fig, ax = plt.subplots()
ax.imshow(data, cmap=cmap, norm=norm)

# draw gridlines
ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1)
ax.set_xticks(np.arange(0.5, rows, 1));
ax.set_yticks(np.arange(0.5, cols, 1));
plt.tick_params(axis='both', labelsize=0, length = 0)
# fig.set_size_inches((8.5, 11), forward=False)
plt.savefig('images/grid.png', dpi=500)
plt.show()
