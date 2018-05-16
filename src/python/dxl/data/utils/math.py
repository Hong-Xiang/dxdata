import numpy as np


def fspecial(size, sigma):
    """Function to mimic the 'fspecial' gaussian MATLAB function.
    :returns result: 2d ndarray, gaussian filter. with shape `[1, size, size, 1]`.
    :type result: Numpy array
    """
    radius = size // 2
    offset = 0.0
    start, stop = -radius, radius + 1
    if size % 2 == 0:
        offset = 0.5
        stop -= 1
    x, y = np.mgrid[offset + start:stop, offset + start:stop]
    assert len(x) == size
    g = np.exp(-((x**2 + y**2) / (2.0 * sigma**2)))
    result = g / g.sum()
    result = result.reshape([result.shape[0], result.shape[1], 1, 1])
    return result
