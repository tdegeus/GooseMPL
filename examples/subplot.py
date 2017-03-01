
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('goose-latex')

x = np.linspace(0,2*np.pi,400)

fig = plt.figure(figsize=(18,6))
fig.set_tight_layout(True)

ax1 = fig.add_subplot(1,2,1)

ax1.plot(x,np.sin(x)         ,label=r'$\sin \big( x \big)$')
ax1.plot(x,np.sin(x-np.pi/4.),label=r'$\sin \big( x - \tfrac{\pi}{4} \big)$')

ax1.set_title('First subplot')

ax1.xaxis.set_ticklabels(['0',r'$\pi$',r'$2\pi$'])
ax1.xaxis.set_ticks([0,np.pi,2*np.pi])
ax1.yaxis.set_ticks([-1,0,1])

plt.legend(loc='upper right')

plt.xlim([0,2*np.pi])

plt.xlabel(r'$x$')
plt.ylabel(r'$y$')

ax2 = fig.add_subplot(1,2,2)

ax2.plot(x,np.cos(x)         ,linestyle='--',label=r'$\cos \big( x \big)$')
ax2.plot(x,np.cos(x-np.pi/4.),linestyle='--',label=r'$\cos \big( x - \tfrac{\pi}{4} \big)$')

ax2.set_title('Second subplot')

ax2.xaxis.set_ticklabels(['0',r'$\pi$',r'$2\pi$'])
ax2.xaxis.set_ticks([0,np.pi,2*np.pi])
ax2.yaxis.set_ticks([-1,0,1])

plt.legend(loc='upper center')

plt.xlim([0,2*np.pi])

plt.xlabel(r'$x$')
plt.ylabel(r'$y$')

plt.savefig('subplot_goose-latex.svg')

