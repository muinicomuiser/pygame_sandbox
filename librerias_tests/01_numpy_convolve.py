import numpy as np
from scipy.signal import convolve2d

array = np.array(
    [
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1],
        [0, 0, 1, 0, 1],
        [0, 0, 1, 0, 1],
        [0, 0, 0, 0, 0],
    ]
)

kernel = np.array(
    [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]
)
result = convolve2d(array, kernel, mode="same", boundary="wrap")
# result = convolve2d(array, kernel, mode='valid', boundary='fill', fillvalue=0)
print(result)
