import numpy as np
import tensorflow as tf


def _ssim_cpu(img1, img2, window, c1, c2):
  from scipy import signal
  from scipy.ndimage.filters import convolve
  from scipy.signal import convolve2d
  window = np.transpose(window, [2, 0, 1, 3])
  mu1 = signal.fftconvolve(img1, window, mode='valid')
  mu2 = signal.fftconvolve(img2, window, mode='valid')
  sigma11 = signal.fftconvolve(img1 * img1, window, mode='valid')
  sigma22 = signal.fftconvolve(img2 * img2, window, mode='valid')
  sigma12 = signal.fftconvolve(img1 * img2, window, mode='valid')
  return _ssim_cpu_post(mu1, mu2, sigma11, sigma22, sigma12, c1, c2)


def _ssim_empty(img1, img2, c1, c2):
  mu1, mu2 = img1, img2
  sigma11 = img1 * img1
  sigma22 = img2 * img2
  sigma12 = img1 * img2
  return _ssim_cpu_post(mu1, mu2, sigma11, sigma22, sigma12, c1, c2)


def _ssim_cpu_post(mu1, mu2, sigma11, sigma22, sigma12, c1, c2):
  mu11 = mu1 * mu1
  mu22 = mu2 * mu2
  mu12 = mu1 * mu2
  sigma11 -= mu11
  sigma22 -= mu22
  sigma12 -= mu12
  v1 = 2.0 * sigma12 + c2
  v2 = sigma11 + sigma22 + c2
  ssim = np.mean(
      (((2.0 * mu12 + c1) * v1) / ((mu11 + mu22 + c1) * v2)), axis=(1, 2, 3))
  cs = np.mean(v1 / v2, axis=(1, 2, 3))
  return ssim, cs


def _ssim_tensorflow(img1, img2, window, c1, c2):
  from dxl.learn.core import Session
  mu1 = tf.nn.conv2d(img1, window, [1] * 4, 'VALID')
  mu2 = tf.nn.conv2d(img2, window, [1] * 4, 'VALID')
  sigma11 = tf.nn.conv2d(img1 * img1, window, [1] * 4, 'VALID')
  sigma22 = tf.nn.conv2d(img2 * img2, window, [1] * 4, 'VALID')
  sigma12 = tf.nn.conv2d(img1 * img2, window, [1] * 4, 'VALID')
  mu11 = mu1 * mu1
  mu22 = mu2 * mu2
  mu12 = mu1 * mu2
  sigma11 -= mu11
  sigma22 -= mu22
  sigma12 -= mu12

  # Calculate intermediate values used by both ssim and cs_map.

  v1 = 2.0 * sigma12 + c2
  v2 = sigma11 + sigma22 + c2
  ssim = tf.reduce_mean(
      (((2.0 * mu12 + c1) * v1) / ((mu11 + mu22 + c1) * v2)), axis=[1, 2, 3])
  cs = tf.reduce_mean(v1 / v2, axis=[1, 2, 3])
  if isinstance(img1, np.ndarray):
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    with tf.Session(config=config) as sess:
      ssim = sess.run(ssim)
      cs = sess.run(cs)
  return ssim, cs


def ssim(img1,
         img2,
         max_val,
         filter_size=11,
         filter_sigma=1.5,
         k1=0.01,
         k2=0.03,
         backend='cpu'):
  """Return the Structural Similarity Map between `img1` and `img2`.
  This function attempts to match the functionality of ssim_index_new.m by
  Zhou Wang: http://www.cns.nyu.edu/~lcv/ssim/msssim.zip
  Arguments:
    img1: Numpy array holding the first RGB image batch.
    img2: Numpy array holding the second RGB image batch.
    max_val: the dynamic range of the images (i.e., the difference between the
      maximum the and minimum allowed values).
    filter_size: Size of blur kernel to use (will be reduced for small images).
    filter_sigma: Standard deviation for Gaussian blur kernel (will be reduced
      for small images).
    k1: Constant used to maintain stability in the SSIM calculation (0.01 in
      the original paper).
    k2: Constant used to maintain stability in the SSIM calculation (0.03 in
      the original paper).
  Returns:
    Pair containing the mean SSIM and contrast sensitivity between `img1` and
    `img2`.
  Raises:
    RuntimeError: If input images don't have the same shape or don't have four
      dimensions: [batch_size, height, width, depth].
  """
  from ..utils import fspecial
  if isinstance(img1, np.ndarray):
    if img1.shape != img2.shape:
      raise RuntimeError('Input images must have the same shape (%s vs. %s).',
                         img1.shape, img2.shape)
    if img1.ndim != 4:
      raise RuntimeError('Input images must have four dimensions, not %d',
                         img1.ndim)
    img1 = img1.astype(np.float32)
    img2 = img2.astype(np.float32)
    _, height, width, _ = img1.shape
  elif isinstance(img1, tf.Tensor):
    _, height, width, _ = img1.shape.as_list()
  size = min(filter_size, height, width)

  # Scale down sigma if a smaller filter size is used.
  sigma = size * filter_sigma / filter_size if filter_size else 0
  c1 = (k1 * max_val)**2
  c2 = (k2 * max_val)**2
  if filter_size:
    window = fspecial(size, sigma)
    if backend == 'cpu':
      return _ssim_cpu(img1, img2, window, c1, c2)
    elif backend == 'tensorflow':
      return _ssim_tensorflow(img1, img2, window, c1, c2)
    raise ValueError("Unknown backend {}.".format(backend))
  else:
    return _ssim_empty(img1, img2, window, c1, c2)
