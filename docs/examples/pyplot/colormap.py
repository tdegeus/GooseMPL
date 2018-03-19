
import numpy             as np
import matplotlib        as mpl
import matplotlib.pyplot as plt

from mpl_toolkits.axes_grid1 import make_axes_locatable

plt.style.use(['goose','goose-latex'])

# total colormap: 500 entries
# - upper part: 400 entries
upper = mpl.cm.jet(np.arange(400))
# - lower part: 100 entries
#   initialize
lower = np.ones((100,4))
#   let range linearly between white (1,1,1) and the first color of the upper colormap
for i in range(3):
  lower[:,i] = np.linspace(1, upper[0,i], lower.shape[0])

# combine parts of colormap
cmap = np.vstack(( lower, upper ))

# convert to matplotlib colormap
cmap = mpl.colors.ListedColormap(cmap, name='myColorMap', N=cmap.shape[0])

# some example
# ------------

# open a new figure
fig, ax = plt.subplots()

# some data to plot: distance to point at (50,50)
x,y = np.meshgrid(np.linspace(0,99,100),np.linspace(0,99,100))
z   = (x-50)**2. + (y-50)**2.

# plot data, apply colormap, set limit such that our interpretation is correct
im = ax.imshow(z, cmap=cmap, clim=(0,5000))

# add a colorbar to the bottom of the image
div  = make_axes_locatable(ax)
cax  = div.append_axes('bottom', size='5%', pad=0.4)
cbar = plt.colorbar(im, cax=cax, orientation='horizontal')

# save/show the image
plt.savefig('colormap.svg')
plt.show()
