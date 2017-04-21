
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

plt.style.use(['goose','latex'])

a,b = np.meshgrid(np.linspace(0,1,100),np.linspace(0,1,100))
d   = np.sqrt(a**2+b**2)

fig  = plt.figure(figsize=(18,6))
fig.set_tight_layout(True)

ax   = fig.add_subplot(1,3,1)
im   = ax.imshow(a,clim=(0,1))
ax.xaxis.set_ticks([0,100])
ax.yaxis.set_ticks([0,100])
plt.xlim([0,100])
plt.ylim([0,100])
plt.xlabel(r'$x$')
plt.ylabel(r'$y$')
plt.title(r'$a$')
div  = make_axes_locatable(ax)
cax  = div.append_axes("right", size="5%", pad=0.1)
cbar = plt.colorbar(im,cax=cax)
cbar.set_ticks([0,1])

ax   = fig.add_subplot(1,3,2)
im   = ax.imshow(b,clim=(0,1))
ax.xaxis.set_ticks([0,100])
ax.yaxis.set_ticks([0,100])
plt.xlim([0,100])
plt.ylim([0,100])
plt.xlabel(r'$x$')
plt.ylabel(r'$y$')
plt.title(r'$b$')
div  = make_axes_locatable(ax)
cax  = div.append_axes("right", size="5%", pad=0.1)
cbar = plt.colorbar(im,cax=cax)
cbar.set_ticks([0,1])

ax   = fig.add_subplot(1,3,3)
im   = ax.imshow(d,clim=(0,1))
ax.xaxis.set_ticks([0,100])
ax.yaxis.set_ticks([0,100])
plt.xlim([0,100])
plt.ylim([0,100])
plt.xlabel(r'$x$')
plt.ylabel(r'$y$')
plt.title(r'$\sqrt{a^2 + b^2}$')
div  = make_axes_locatable(ax)
cax  = div.append_axes("right", size="5%", pad=0.1)
cbar = plt.colorbar(im,cax=cax)
cbar.set_ticks([0,1])

plt.savefig('image_subplots.svg')
