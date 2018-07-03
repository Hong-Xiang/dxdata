from dxl.data.function import To
import numpy as np


def test_to_ndarray():
    x = To(np.array)([1, 2, 3])
    assert isinstance(x, np.ndarray)
    assert x.shape == (3,)
