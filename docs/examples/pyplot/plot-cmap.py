import numpy             as np
import matplotlib        as mpl
import matplotlib.pyplot as plt

plt.style.use(['goose','goose-latex'])

x      = np.linspace(0, 5, 100)
N      = 21
cmap   = plt.get_cmap('jet',N)

fig,ax = plt.subplots()
# N.B. to modify the aspect ratio one could replace this line by:
# fig = plt.figure(figsize=(8,6))
# ax1 = fig.add_axes([0.10,0.10,0.70,0.85])

for i,n in enumerate(np.linspace(0,2,N)):
  y = np.sin(x)*x**n
  ax.plot(x,y,color=cmap(i))

plt.xlabel(r'$x$')
plt.ylabel(r'$y$')

norm = mpl.colors.Normalize(vmin=0,vmax=2)
sm   = plt.cm.ScalarMappable(cmap=cmap,norm=norm)
sm.set_array([])
plt.colorbar(sm,ticks=np.linspace(0,2,N),boundaries=np.arange(-0.05,2.1,.1))

plt.savefig('plot-cmap.svg')
plt.show()
