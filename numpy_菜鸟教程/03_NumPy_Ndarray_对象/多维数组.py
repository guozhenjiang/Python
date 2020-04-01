# import numpy as np
# a = np.array([  [[1, 2], [3, 4]],\
#                 [[1, 2], [3, 4]],\
#                 [[1, 2], [3, 4]],   ])
# print(a)

import numpy as np
a = np.arange(1 * 2 * 3 * 4 * 5)
print(a)

b = a.reshape(1, 2, 3, 4, 5)
print(b)