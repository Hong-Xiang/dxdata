from ._base import PersistentData, PersistentDataInDataset
from abc import ABCMeta, abstractmethod, abstractproperty


class ArrayND:
  def __init__(self, data):
    self._data = data

  def data(self):
    """
    Unboxing data.
    """
    return self._data

  @property
  def shape(self):
    return self._data.shape

  @property
  def ndim(self):
    return self._data.ndim

  def __getitem__(self, val):
    return self._data[val]


class ArrayNDHDF5(PersistentDataInDataset, ArrayND):
  def __init__(self, path_file, path_in_dataset):
    PersistentDataInDataset.__init__(self, path_file, path_in_dataset)
    ArrayND.__init__(self, None)

  def __enter__(self):
    pass
