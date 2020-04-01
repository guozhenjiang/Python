import numpy as np
import matplotlib.pyplot as plt
t1 = np.arange(0, 5, 0.1)
t2 = np.arange(0, 10, 0.2)
t3 = np.arange(0, 20, 0.4)
t4 = np.arange(0, 40, 0.8)
 
plt.subplot(221)
plt.plot(t1, t2, 'r--')
plt.subplot(222)
plt.plot(t1, t3, 'b--')
plt.subplot(212)
plt.plot(t1, t4, 'g--')
plt.show()