import unittest
from dxl.data.geometry.ndspace import Points, grid_index, inbound_mask, GridSpec
import numpy as np


class TestFunctions(unittest.TestCase):
    def test_grid_index_and_inbound_mask(self):
        data = [[1.0, 2.0, 3.0],
                [1.5, 2.5, 3.5],
                [1.0, 2.0, 5.0]]
        grid_spec = GridSpec([1.0, 1.0, 1.0],
                             [4.0, 4.0, 4.0],
                             [1.0, 1.0, 1.0])
        index = grid_index(data, grid_spec)
        mask = inbound_mask(data, grid_spec)
        index = index[mask, :]
        self.assertTrue(np.array_equal(index,
                                       np.array([[0, 1, 2], [0, 1, 2]])))
