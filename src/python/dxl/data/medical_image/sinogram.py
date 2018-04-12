import numpy as np
from typing import Tuple


class Sinogram2D:
  def __init__(self, data: np.ndarray):
    """
    Sinogram2D processings.

    :param data: Raw sinogram, 2 dimensional array, in the order [0..nb_views, 0..nb_sensors]
    :type data: NumPy array
    """
    self._data = np.array(data)

  @property
  def d(self):
    return self._data

  def crop(self, x_crops: Tuple[int, int],
           y_crops: Tuple[int, int] = None) -> 'Sinogram2D':
    if isinstance(x_crops, int):
      x_crops = (x_crops, x_crops)
    if isinstance(y_crops, int):
      y_crops = (y_crops, y_crops)
    if x_crops[1] > 0 and y_crops[1] > 0:
      return Sinogram2D(self.d[x_crops[0]:-x_crops[1], y_crops[0]:-y_crops[1]])
    if x_crops[1] > 0:
      return Sinogram2D(self.d[x_crops[0]:-x_crops[1], y_crops[0]:])
    if y_crops[1] > 0:
      return Sinogram2D(self.d[x_crops[0]:, y_crops[0]:-y_crops[1]])
    return Sinogram2D(self.d[x_crops[0]:, y_crops[0]:])