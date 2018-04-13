import numpy as np
from pathlib import Path
class DataOnFS:
  pass

class NDArrayOnFS:
  """
  Data stored in filesyte, but is convertable to ndarray.
  Currently support following data types:
  1. .npy, requires path
  2. .npz, requires path, in_file_path or dataset
  3. .h5, requires path, in_file_path or dataset 
  """

  def __init__(self, path:Path, in_file_path:Path=None, dataset:str=None)
    self._path = Path(path)
    self._in_file_path = Path(in_file_path)
    self._dataset = str(dataset)
    self._data = None

  @property
  def shape(self):
    pass
  
  @property
  def ndim(self):
    pass
