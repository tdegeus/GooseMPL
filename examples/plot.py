
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0,2*np.pi,400)

# ==============================================================================
# default
# ==============================================================================

fig,ax = plt.subplots()

ax.plot(x,np.sin(x)         ,label=r'sin x')
ax.plot(x,np.sin(x-np.pi/4.),label=r'sin x - $\pi$/4')

ax.set_title('Simple plot')

ax.xaxis.set_ticklabels(['0',r'$\pi$',r'$2\pi$'])
ax.xaxis.set_ticks([0,np.pi,2*np.pi])
ax.yaxis.set_ticks([-1,0,1])

plt.legend(loc='upper right')

plt.xlim([0,2*np.pi])

plt.xlabel(r'x')
plt.ylabel(r'y')

plt.savefig('plot.svg')

# ==============================================================================
# goose
# ==============================================================================

plt.style.use('goose')

fig,ax = plt.subplots()

ax.plot(x,np.sin(x)         ,label=r'sin x')
ax.plot(x,np.sin(x-np.pi/4.),label=r'sin x - $\pi$/4')

ax.set_title('Simple plot')

ax.xaxis.set_ticklabels(['0',r'$\pi$',r'$2\pi$'])
ax.xaxis.set_ticks([0,np.pi,2*np.pi])
ax.yaxis.set_ticks([-1,0,1])

plt.legend(loc='upper right')

plt.xlim([0,2*np.pi])

plt.xlabel('x')
plt.ylabel('y')

plt.savefig('plot_goose.svg')

# ==============================================================================
# goose-latex
# ==============================================================================

plt.style.use(['goose','goose-latex'])

fig,ax = plt.subplots()

ax.plot(x,np.sin(x)         ,label=r'$\sin \big( x \big)$')
ax.plot(x,np.sin(x-np.pi/4.),label=r'$\sin \big( x - \tfrac{\pi}{4} \big)$')

ax.set_title('Simple plot')

ax.xaxis.set_ticklabels(['0',r'$\pi$',r'$2\pi$'])
ax.xaxis.set_ticks([0,np.pi,2*np.pi])
ax.yaxis.set_ticks([-1,0,1])

plt.legend(loc='upper right')

plt.xlim([0,2*np.pi])

plt.xlabel(r'$x$')
plt.ylabel(r'$y$')

plt.savefig('plot_goose-latex.svg')

