# see : http://matplotlib.org/examples/api/colorbar_only.html

import matplotlib.pyplot as plt
import matplotlib        as mpl

plt.style.use(['goose','goose-latex'])

fig,ax = plt.subplots(figsize=(2, 8))

cbar = mpl.colorbar.ColorbarBase(ax,
  cmap        = mpl.cm.get_cmap('RdBu_r'),
  norm        = mpl.colors.Normalize(vmin=5, vmax=10),
  orientation = 'vertical'
)

cbar.set_label('Some Units')

plt.savefig('colorbar.svg')
plt.show()
