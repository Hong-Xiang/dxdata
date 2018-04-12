import unittest
import numpy as np
from dxl.data.statistics.image import msssim


class TestMSSSIMCPU(unittest.TestCase):
  def test_basic(self):
    img0 = np.arange(256 * 256).reshape([1, 256, 256, 1]).astype(
        np.float32) / 256.0
    img1 = img0.T
    result = msssim(img0, img1, 255, backend='cpu')
    expected = 0.32705
    self.assertEqual(result.shape, (1, ))
    self.assertAlmostEqual(result[0], expected, places=4)


class TestMSSSIMTensorflow(unittest.TestCase):
  def test_basic(self):
    img0 = np.arange(256 * 256).reshape([1, 256, 256, 1]).astype(
        np.float32) / 256.0
    img1 = img0.T
    result = msssim(img0, img1, 255, backend='tensorflow')
    expected = 0.32705
    self.assertEqual(result.shape, (1, ))
    self.assertAlmostEqual(result[0], expected, places=4)
