import numpy as np
import matplotlib.pyplot as plt
 
t1 = np.arange(0, 5, 0.1)
t2 = np.arange(0, 10, 0.2)
 
plt.plot(t1, t1, 'r--')
plt.plot(t1, t2, 'b--')
plt.show()