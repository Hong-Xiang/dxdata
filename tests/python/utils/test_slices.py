import unittest
import numpy as np
import dxl.data.utils.slices as slices


class TestSlicesFromStr(unittest.TestCase):
    def test_parse_str(self):
        self.assertEqual(slices._parse_single_str_slice('1:2'), slice(1, 2))

    def test_basic_1(self):
        a = np.arange(49).reshape([7] * 2)
        res = a[slices.slices_from_str('[2:5,-3:-1]')]
        np.testing.assert_array_equal(res,
                                      np.array([[18, 19], [25, 26], [32, 33]]))

    def test_basic_2(self):
        a = np.arange(49).reshape([7] * 2)
        res = a[slices.slices_from_str('[2:5,3:4]')]
        np.testing.assert_array_equal(res, np.array([[17], [24], [31]]))

    def test_basic_3(self):
        a = np.arange(49).reshape([7] * 2)
        res = a[slices.slices_from_str('[1:2,6]')]
        np.testing.assert_array_equal(res, np.array([13]))
