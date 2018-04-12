import numpy as np


def rmse(label, target):
  err = target - label
  value = np.sqrt(np.sum(np.square(err)) / label.size)
  # base = np.sqrt(np.sum(np.square(target)) / label.size)
  # return value / base
  return value


def mean_absolute_error(label, target):
  err = target - label
  return np.mean(np.abs(err))


def bias(label, target):
  return np.mean(label - target)


def variance(label, target):
  return np.std(label - target)


def psnr(label, target):
  minv = np.min(label)
  maxv = np.max(label)
  sca = 255.0 / (maxv - minv)
  ln = (label - minv) * sca
  tn = (target - minv) * sca
  rmv = rmse(ln, tn)
  value = 10 * np.log((255.0**2) / (rmv**2)) / np.log(10)
  return value
