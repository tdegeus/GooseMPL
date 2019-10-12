
import numpy as np
import matplotlib.pyplot as plt

plt.style.use(['goose', 'goose-latex'])

# --- some data ---

x = np.linspace(0,2*np.pi,400)

# --- open figure with 2 subplots ---

fig, axes = plt.subplots(ncols=2, figsize=(18,6))

ax1 = axes[0]
ax2 = axes[1]

# --- first subplot ---

ax1.plot(x,np.sin(x)         ,label=r'$\sin \big( x \big)$')
ax1.plot(x,np.sin(x-np.pi/4.),label=r'$\sin \big( x - \tfrac{\pi}{4} \big)$')

ax1.set_title('First subplot')

ax1.xaxis.set_ticklabels(['0',r'$\pi$',r'$2\pi$'])
ax1.xaxis.set_ticks([0,np.pi,2*np.pi])
ax1.yaxis.set_ticks([-1,0,1])

ax1.legend(loc='upper right')

ax1.set_xlim([0,2*np.pi])

ax1.set_xlabel(r'$x$')
ax1.set_ylabel(r'$y$')

# --- second subplot ---

ax2.plot(x,np.cos(x)         ,linestyle='--',label=r'$\cos \big( x \big)$')
ax2.plot(x,np.cos(x-np.pi/4.),linestyle='--',label=r'$\cos \big( x - \tfrac{\pi}{4} \big)$')

ax2.set_title('Second subplot')

ax2.xaxis.set_ticklabels(['0',r'$\pi$',r'$2\pi$'])
ax2.xaxis.set_ticks([0,np.pi,2*np.pi])
ax2.yaxis.set_ticks([-1,0,1])

ax2.legend(loc='upper center')

ax2.set_xlim([0,2*np.pi])

ax2.set_xlabel(r'$x$')
ax2.set_ylabel(r'$y$')

# --- save/show ---

plt.savefig('subplot.svg')
plt.show()

