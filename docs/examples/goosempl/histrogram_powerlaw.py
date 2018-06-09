
import matplotlib.pyplot as plt
import goosempl          as gplt
import numpy             as np

plt.style.use(['goose','goose-latex'])

# ------------------------------------------------------------------------------

def distribution(a=100, b=3, g=-.3, size=10000):

  r = np.random.random(size=size)

  return (a**g + (b**g - a**g)*r)**(1./g)

# ------------------------------------------------------------------------------

data = distribution()

fig, axes = plt.subplots(ncols=3, figsize=(24,8))

P,x = gplt.histogram(data, bins=41, x='mid', density=True)

axes[0].plot(x,P,marker='o', linestyle='none', markersize=5., color='k')

axes[0].set_title(r'histogram')

P,x = gplt.histogram_log(data, bins=41, x='mid', density=True)

axes[1].plot(x,P,marker='o', linestyle='none', markersize=5., color='b')

axes[1].set_title(r'histogram\_log')

P,x = gplt.histogram_uniform(data, bins=41, x='mid', density=True)

axes[2].plot(x,P,marker='o', linestyle='none', markersize=5., color='r')

axes[2].set_title(r'histogram\_uniform')

for ax in axes:

  ax.set_xlabel(r'$x$')
  ax.set_ylabel(r'$\rho(x)$')

  ax.set_xscale('log')
  ax.set_yscale('log')

  ax.set_xlim([10**0   , 10**3])
  ax.set_ylim([10**(-3), 10**0])

plt.savefig('histrogram_powerlaw.svg')
plt.show()
