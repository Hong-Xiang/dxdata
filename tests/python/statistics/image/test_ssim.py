import unittest
from dxl.data.statistics.image import ssim

class TestSSIMCPU(unittest.TestCase):
  def test_basic(self):
    img0 = np.arange(256*256).reshape([1, 256, 256, 1]).astype(np.float32)/256.0
    img1 = img0.T
    result = ssim(img0, img1, 255, backend='cpu')

