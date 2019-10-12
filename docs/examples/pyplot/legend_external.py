
import numpy as np
import matplotlib.pyplot as plt

plt.style.use(['goose', 'goose-latex'])

fig, ax = plt.subplots(figsize=(9,6))

x = np.arange(10)

for i in range(5):
  ax.plot(x, i*x, label='$y = {:d}x$'.format(i))

legend = ax.legend(loc='center left', bbox_to_anchor=(1., 0.5), fancybox=True, shadow=True)

frame = legend.get_frame()
frame.set_facecolor('white')
frame.set_edgecolor('black')

plt.savefig('legend_external.svg')
plt.show()
