# import numpy as np
# import scipy
# #from scipy import signal

# import matplotlib.pyplot as plt

# t = np.loadtxt("data.txt")
# print(t)
# plt.plot(t)
# plt.show()

# import scipy
# print(scipy.__version__)

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

a = np.array([1, 2, 3, 4, 5])

np.save('out.npy', a)
np.save('outtxt.txt', a)

# t = np.load('out.npy')
t = np.loadtxt('data.txt')
# t = np.loadtxt('outtxt.txt')
print(t)

plt.plot(t)
plt.show()
