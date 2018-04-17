import numpy as np
from scipy import signal
import tensorflow as tf

from ..utils import fspecial
from ._ssim import ssim


def _msssim_common(img1, img2, max_val, filter_size, filter_sigma, k1, k2,
                   weights, backend):
  levels = weights.size
  mssim = []
  mcs = []
  if backend == 'cpu':
    g = _msssim_cpu
  else:
    g = _msssim_tensorflow
  for im1, im2 in g(img1, img2, levels):
    _ssim, _cs = ssim(
        im1,
        im2,
        max_val=max_val,
        filter_size=filter_size,
        filter_sigma=filter_sigma,
        k1=k1,
        k2=k2,
        backend=backend)
    mssim.append(_ssim)
    mcs.append(_cs)
  result = 1.0
  for mc, w in zip(mcs[:-1], weights[:-1]):
    result = result * mc**w
  result = result * mssim[-1]**weights[-1]
  if isinstance(result, tf.Tensor):
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    with tf.Session(config=config) as sess:
      result = sess.run(result)
  return result


def _msssim_cpu(img1, img2, levels):
  from scipy.ndimage.filters import convolve
  downsample_filter = np.ones((1, 2, 2, 1)) / 4.0
  im1, im2 = [x.astype(np.float64) for x in [img1, img2]]
  for _ in range(levels):
    yield im1, im2
    filtered = [
        convolve(im, downsample_filter, mode='reflect') for im in [im1, im2]
    ]
    im1, im2 = [x[:, ::2, ::2, :] for x in filtered]


def _msssim_tensorflow(img1, img2, levels):
  downsample_filter = np.ones((2, 2, 1, 1)) / 4.0
  im1, im2 = [tf.constant(x, dtype=tf.float32) for x in [img1, img2]]
  for _ in range(levels):
    yield im1, im2
    filtered = [
        tf.nn.conv2d(im, downsample_filter, [1, 2, 2, 1], 'SAME')
        for im in [im1, im2]
    ]
    im1, im2 = filtered


def msssim(img1,
           img2,
           max_val=255,
           filter_size=11,
           filter_sigma=1.5,
           k1=0.01,
           k2=0.03,
           weights=None,
           backend=None):
  """Return the MS-SSIM score between `img1` and `img2`.
  This function implements Multi-Scale Structural Similarity (MS-SSIM) Image
  Quality Assessment according to Zhou Wang's paper, "Multi-scale structural
  similarity for image quality assessment" (2003).
  Link: https://ece.uwaterloo.ca/~z70wang/publications/msssim.pdf
  Author's MATLAB implementation:
  http://www.cns.nyu.edu/~lcv/ssim/msssim.zip
  Arguments:
    img1: Numpy array holding the first RGB image batch.
    img2: Numpy array holding the second RGB image batch.
    max_val: the dynamic range of the images (i.e., the difference between the
      maximum the and minimum allowed values).
    filter_size: Size of blur kernel to use (will be reduced for small images).
    filter_sigma: Standard deviation for Gaussian blur kernel (will be reduced
      for small images)
    k1: Constant used to maintain stability in the SSIM calculation (0.01 in
      the original paper).
    k2: Constant used to maintain stability in the SSIM calculation (0.03 in
      the original paper).
    weights: List of weights for each level; if none, use five levels and the
      weights from the original paper.
  Returns:
    MS-SSIM score between `img1` and `img2`.
  Raises:
    RuntimeError: If input images don't have the same shape or don't have four
      dimensions: [batch_size, height, width, depth].
  """
  if backend is None:
    backend = 'cpu'
  if img1.shape != img2.shape:
    raise RuntimeError('Input images must have the same shape (%s vs. %s).',
                       img1.shape, img2.shape)
  if img1.ndim != 4:
    raise RuntimeError('Input images must have four dimensions, not %d',
                       img1.ndim)

  # Note: default weights don't sum to 1.0 but do match the paper / matlab code.
  weights = np.array(weights
                     if weights else [0.0448, 0.2856, 0.3001, 0.2363, 0.1333])
  return _msssim_common(img1, img2, max_val, filter_size, filter_sigma, k1, k2,
                        weights, backend)
