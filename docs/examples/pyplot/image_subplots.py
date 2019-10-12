
import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.axes_grid1 import make_axes_locatable

plt.style.use(['goose', 'goose-latex'])

# --- some data ----

a, b = np.meshgrid(np.linspace(0, 1, 100), np.linspace(0, 1, 100))
d = np.sqrt(a**2 + b**2)

# --- open figure with three axes ---

fig, axes  = plt.subplots(ncols=3, figsize=(18, 6))

# --- left subplot ---

ax = axes[0]
im = ax.imshow(a, clim=(0, 1))
ax.xaxis.set_ticks([0, 100])
ax.yaxis.set_ticks([0, 100])
ax.set_xlim([0, 100])
ax.set_ylim([0, 100])
ax.set_xlabel(r'$x$')
ax.set_ylabel(r'$y$')
ax.set_title(r'$a$')
div  = make_axes_locatable(ax)
cax  = div.append_axes('right', size='5%', pad=0.1)
cbar = plt.colorbar(im, cax=cax)
cbar.set_ticks([0, 1])

# --- middle subplot ---

ax = axes[1]
im = ax.imshow(b, clim=(0, 1))
ax.xaxis.set_ticks([0, 100])
ax.yaxis.set_ticks([0, 100])
ax.set_xlim([0, 100])
ax.set_ylim([0, 100])
ax.set_xlabel(r'$x$')
ax.set_ylabel(r'$y$')
ax.set_title(r'$b$')
div  = make_axes_locatable(ax)
cax  = div.append_axes('right', size='5%', pad=0.1)
cbar = plt.colorbar(im, cax=cax)
cbar.set_ticks([0, 1])

# --- right subplot ---

ax = axes[2]
im = ax.imshow(d, clim=(0, 1))
ax.xaxis.set_ticks([0, 100])
ax.yaxis.set_ticks([0, 100])
ax.set_xlim([0, 100])
ax.set_ylim([0, 100])
ax.set_xlabel(r'$x$')
ax.set_ylabel(r'$y$')
ax.set_title(r'$\sqrt{a^2 + b^2}$')
div  = make_axes_locatable(ax)
cax  = div.append_axes('right', size='5%', pad=0.1)
cbar = plt.colorbar(im, cax=cax)
cbar.set_ticks([0, 1])

# --- save/show ---

plt.savefig('image_subplots.svg')
plt.show()
