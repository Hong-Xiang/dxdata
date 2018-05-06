from ._base import PersistentData, PersistentDataInDataset
from abc import ABCMeta, abstractmethod, abstractproperty
import h5py
import numpy as np


class NDArray:
    def __init__(self, data, slices=None):
        self._data = data
        self._slices = slices

    def data(self):
        """
        Unboxing data.
        """
        return self._data

    def to_numpy_ndarray(self):
        d = self.data()
        if isinstance(d, np.ndarray):
            return d
        else:
            return np.array(d)

    @property
    def shape(self):
        return self._data.shape

    @property
    def ndim(self):
        return self._data.ndim

    def __getitem__(self, val):
        return self._data[val]


class NDArrayHDF5(PersistentDataInDataset, NDArray):
    """
    Provide an abstract layer of dataset/ndarray object in HDF5 file.
    Currently support:

    - `self.shape`
    - `self.ndim`
    - `self[slices]`
    
    Load data lazily, thus only after `self.data()` is called,
    the whole array is loaded into memory.
    """

    def __init__(self, path_file, path_dataset, slices=None):
        """
        """
        PersistentDataInDataset.__init__(self, path_file, path_dataset)
        # Lazy loading data. Thus NDArray is initilized with `data` = None
        NDArray.__init__(self, None, slices)

    def data(self):
        if self._data is None:
            from dxl.data.io import load_h5
            self._data = load_h5(self.path, self.path_dataset, self._slices)
        return self._data

    def _apply_to_h5dataset_if_data_is_none(self, func):
        if self._data is None:
            with h5py.File(self.path, 'r') as fin:
                return func(fin[self.path_dataset])
        else:
            return func(fin[self._data])

    @property
    def shape(self):
        return self._apply_to_h5dataset_if_data_is_none(lambda d: d.shape)

    @property
    def ndim(self):
        return self._apply_to_h5dataset_if_data_is_none(lambda d: d.ndim)

    def __getitem__(self, val):
        return self._apply_to_h5dataset_if_data_is_none(lambda d: d[val])


__all__ = ['NDArrayHDF5']