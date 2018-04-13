import numpy as np


def rmse_(label, target):
  err = target - label
  value = np.sqrt(np.sum(np.square(err)) / label.size)
  # base = np.sqrt(np.sum(np.square(target)) / label.size)
  # return value / base
  return value


def mean_absolute_error_(label, target):
  err = target - label
  return np.mean(np.abs(err))


def bias_(label, target):
  return np.mean(label - target)


def variance_(label, target):
  return np.std(label - target)


def psnr_(label, target):
  minv = np.min(label)
  maxv = np.max(label)
  sca = 255.0 / (maxv - minv)
  ln = (label - minv) * sca
  tn = (target - minv) * sca
  rmv = rmse(ln, tn)
  value = 10 * np.log((255.0**2) / (rmv**2)) / np.log(10)
  return value


def _map_batch(func, label, target):
  nb_images = label.shape[0]
  result = [
      func(label[i, :, :, 0], target[i, :, :, 0]) for i in range(nb_images)
  ]
  return np.array(result)


def _unified_dim_2_and_4(func, label, target):
  if label.ndim == 2:
    return func(label, target)
  elif label.ndim == 4:
    return _map_batch(func, label, target)
  raise ValueError("Invalid shape: {}.".format(label.shape))


def psnr(label, target):
  return _unified_dim_2_and_4(psnr_, label, target)


def rmse(label, target):
  return _unified_dim_2_and_4(rmse_, label, target)


def mean_absolute_error(label, target):
  return _unified_dim_2_and_4(mean_absolute_error_, label, target)


def variance(label, target):
  return _unified_dim_2_and_4(variance_, label, target)


def bias(label, target):
  return _unified_dim_2_and_4(bias_, label, target)