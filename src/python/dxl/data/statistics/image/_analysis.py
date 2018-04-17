import numpy as np
import pandas as pd
from ._ssim import ssim
from ._msssim import msssim
from ._basic import psnr, rmse


def _metrics_name(m):
  return {
      psnr: 'psnr',
      rmse: 'rmse',
      ssim: 'ssim',
      msssim: 'msssim',
      np.mean: 'mean',
      np.max: 'max',
      np.min: 'min',
      np.std: 'std'
  }[m]


def crop(value, vmin=0.0, vmax=None):
  if vmin is not None:
    value = np.minimum(value, vmin)
  if vmax is not None:
    value = np.maximum(value, vmax)
  return value


def rescale(target, label=None, k=None, bias=None, vkeep=None):
  if vkeep is None:
    vkeep = 0.0
  if label is not None:
    k = np.mean(label - vkeep) / np.mean(target - vkeep)
    if abs(k) > 1e-5:
      bias = (vkeep - k * vkeep) / k
  return k * (target + bias)


def compare_analysis(label,
                     target,
                     metrics=tuple(),
                     *,
                     max_val=None,
                     backend=None):
  if label.ndim != 4:
    raise ValueError("Label should has shape [N,H,W,C], got {}.".format(
        label.shape))
  if target.ndim != 4:
    raise ValueError("Target should has shape [N,H,W,C], got {}.".format(
        target.shape))
  if label.shape != target.shape:
    raise ValueError(
        "Label and target should have same shape, got label: {}, target: {}.".
        format(label.shape, target.shape))
  if max_val is None:
    max_val = np.max(label)
  results = {}
  for m in metrics:
    name = _metrics_name(m)
    if m in (psnr, rmse):
      result = m(label, target)
    elif m in (ssim, msssim):
      result = m(label, target, max_val=max_val, backend=backend)
    else:
      raise ValueError("Unknown metric {}.".format(m))
    results[name] = np.array(result)
  return pd.DataFrame(data=results)


def single_analysis(target, metrics=(np.mean, np.min, np.max, np.std)):
  if target.ndim != 4:
    raise ValueError("Target should has shape [N,H,W,C], got {}.".format(
        target.shape))
  nb_images = target.shape[0]
  results = {}
  for m in metrics:
    name = _metrics_name(m)
    if m in (np.mean, np.max, np.min, np.std):
      results[name] = m(target, axis=(1, 2, 3))
  return pd.DataFrame(data=results)
