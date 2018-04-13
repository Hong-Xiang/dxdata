import unittest
import numpy as np
from dxl.data.statistics.image import ssim


class TestSSIMCPU(unittest.TestCase):
  def test_basic(self):
    img0 = np.arange(256 * 256).reshape([1, 256, 256, 1]).astype(
        np.float32) / 256.0 / 256.0 * 255.0
    img1 = img0.T
    ssim_, mcs_ = ssim(img0, img1, 255, backend='cpu')
    expected = (0.6688, 0.9298)
    self.assertEqual(ssim_.shape, (1, ))
    self.assertEqual(mcs_.shape, (1, ))
    self.assertAlmostEqual(ssim_[0], expected[0], places=3)
    self.assertAlmostEqual(mcs_[0], expected[1], places=3)


class TestSSIMTensorflow(unittest.TestCase):
  def test_basic(self):
    img0 = np.arange(256 * 256).reshape([1, 256, 256, 1]).astype(
        np.float32) / 256.0 / 256.0 * 255.0
    img1 = img0.T
    ssim_, mcs_ = ssim(img0, img1, 255, backend='tensorflow')
    expected = (0.6688, 0.9298)
    self.assertEqual(ssim_.shape, (1, ))
    self.assertEqual(mcs_.shape, (1, ))
    self.assertAlmostEqual(ssim_[0], expected[0], places=3)
    self.assertAlmostEqual(mcs_[0], expected[1], places=3)
