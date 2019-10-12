
import numpy as np
import matplotlib.pyplot as plt

plt.style.use(['goose', 'goose-latex'])

x = np.linspace(0,2*np.pi,400)

fig,ax = plt.subplots()

ax.plot(x,np.sin(x)         ,label=r'$\sin \big( x \big)$')
ax.plot(x,np.sin(x-np.pi/4.),label=r'$\sin \big( x - \tfrac{\pi}{4} \big)$')

ax.set_title('Simple plot')

ax.xaxis.set_ticklabels(['0',r'$\pi$',r'$2\pi$'])
ax.xaxis.set_ticks([0,np.pi,2*np.pi])
ax.yaxis.set_ticks([-1,0,1])

ax.legend(loc='upper right')

ax.set_xlim([0,2*np.pi])

ax.set_xlabel(r'$x$')
ax.set_ylabel(r'$y$')

plt.savefig('plot.svg')
plt.show()

