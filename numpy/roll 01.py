import numpy as np

x = np.arange(10)
print('\r\n np.arange(10):', x)

x = np.roll(x, 2)
print('\r\n np.roll(x, 2)', x)

x = np.roll(x, -2)
print('\r\n np.roll(x, -2)', x)

'''
np.arange(10): [0 1 2 3 4 5 6 7 8 9]

 np.roll(x, 2) [8 9 0 1 2 3 4 5 6 7]

 np.roll(x, -2) [0 1 2 3 4 5 6 7 8 9]
'''