
import matplotlib.pyplot as plt
import GooseMPL          as gplt
import numpy             as np

plt.style.use(['goose','goose-latex'])

# ------------------------------------------------------------------------------

def distribution(a=100, b=3, g=-.3, size=10000):

  r = np.random.random(size=size)

  return (a**g + (b**g - a**g)*r)**(1./g)

# ------------------------------------------------------------------------------

data = distribution()

fig, axes = plt.subplots(ncols=3, figsize=(24,8))

# configure axes

for ax in axes:

  ax.set_xlabel(r'$x$')
  ax.set_ylabel(r'$\rho(x)$')

  ax.set_xscale('log')
  ax.set_yscale('log')

  ax.set_xlim([10**0   , 10**3])
  ax.set_ylim([10**(-3), 10**0])

# histogram

P,x = gplt.histogram(data, bins=41, density=True, return_edges=False)

axes[0].plot(x,P,marker='o', linestyle='none', markersize=5., color='k')

# histogram_log

P,x = gplt.histogram_log(data, bins=41, density=True, return_edges=False)

axes[1].plot(x,P,marker='o', linestyle='none', markersize=5., color='b')

# histogram_uniform

P,x = gplt.histogram_uniform(data, bins=41, density=True, return_edges=False)

axes[2].plot(x,P,marker='o', linestyle='none', markersize=5., color='r')

# add titles

axes[0].set_title(r'histogram')
axes[1].set_title(r'histogram\_log')
axes[2].set_title(r'histogram\_uniform')

# annotate powerlaw in different ways

for ax in axes:

  gplt.grid_powerlaw(exp=-1.3, axis=ax)

  gplt.plot_powerlaw(               exp=-1.3, startx=.4, starty=.5, width=.2, axis=ax, units='relative')
  gplt.annotate_powerlaw(r'$-1.3$', exp=-1.3, startx=.4, starty=.5, width=.2, axis=ax, units='relative', rx=.55)

plt.savefig('histogram_powerlaw.svg')
plt.show()
