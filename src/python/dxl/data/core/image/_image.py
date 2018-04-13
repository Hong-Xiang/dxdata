import numpy as np


class Image:
  """
  with data shape [H, W, 3] or [H, W, 1]
  """

  def __init__(self, data):
    self._data = data


class Images:
  """
  with data shape [N, H, W, C]
  """
  pass


class ImagesGrid:
  """
  with data shape [R, C][H, W, C], for visualization use only.
  """
  pass