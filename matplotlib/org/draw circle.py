"""
http://matplotlib.org/api/artist_api.html
"""
import matplotlib.pyplot as plt

plt.rcdefaults()

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches

fig = plt.figure()

ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 4)

data = [1, 2, 3, 4]

ax1.plot([1, 2, 3, 4], 'or')
ax2.plot([2, 3, 4, 5], 'ob')

ax1.set_gid(True)

# ax2.set_visible(False)
# ax1.set_visible(True)
# ax2.remove()

plt.show()