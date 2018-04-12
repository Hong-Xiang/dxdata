import numpy as np


def __guess_shape(length, ndim=None):
  if length == 1 and (ndim is None or ndim == 0):
    return []
  if ndim is None:
    return [length]
  size = int(np.ceil(np.power(length, 1 / ndim)))
  if size**ndim == length:
    return [size] * ndim
  raise ValueError("Cannot guess shape of length {} with ndim {}.".format(
      length, ndim))


def load_bin(filename, shape=None, dtype=np.float32, *, fs=None, ndim=None):
  open_func = open if fs is None else fs.open
  with open_func(filename, 'rb') as fin:
    raw_data = np.fromstring(fin.read(), dtype)
  if shape is None:
    shape = __guess_shape(raw_data.size, ndim)
  return np.reshape(raw_data, shape)


def save_bin(filename, tensor, dtype=np.float32):
  tensor = tensor.astype(dtype)
  raw_data = tensor.tostring()
  with open(filename, 'wb') as fout:
    fout.write(raw_data)
