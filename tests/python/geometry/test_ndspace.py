import unittest
from dxl.data.geometry.ndspace import Points
import numpy as np

class TestPoints(unittest.TestCase):
    def test_histogram(self):
        data = [[1.0, 2.0, 3.0],
                [1.5, 2.5, 3.5],
                [1.0, 2.0, 5.0]]
        points = Points(data)
        hist3 = points.histogram([1.0, 1.0, 1.0],
                                 [4.0, 4.0, 4.0],
                                 [1.0, 1.0, 1.0])
        self.assertTrue(np.array_equal(hist3.data(),
                                       np.array([[0, 1, 2], [0, 1, 2]])))
