import numpy as np


class Image:
  """
  Unified Image object, with data shape [H, W, 3] or [H, W, 1].
  """

  @classmethod
  def boxing(cls, data):
    pass

  @classmethod
  def unboxing(cls, data):
    pass

  def __init__(self, data):
    self._data = data


class StackedImages:
  """
  with data shape [N, H, W, C]
  """

  def __init__(self, data):
    """
    :type data: numpy.ndarray or dxl.data.Image 
    """
    self._data = data

  def _load_data(self):
    if isinstance(data, Image):
      self._data = data.reshape([1] + list(data.shape))
    if isinstance(data, (list, tuple)):
      if isinstance(data[0], Image):
        self._data = np.array()

  def ndim(self):
    return self._data.ndim


class DictOfStackedImages:
  def __init__(self, data):
    self._data = self._unified_data(data)

  def _unified_data(self, data):
    if isinstance(data, dict):
      result = {}
      for k, v in data.items():
        if v.ndim == 3:
          result[k] = np.expand_dims(v, 3)
        else:
          result[k] = v
      return result
    else:
      return data

  def data(self):
    return self._data

  def shape(self):
    return {k: self.data()[k].shape for k in self.data()}

  def ndim(self):
    return {k: self.data()[k].ndim for k in self.data()}


class ImagesGrid:
  """
  with data shape [R, C][H, W, C], for visualization use only.
  """
  pass