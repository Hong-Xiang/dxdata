from ..utils.slices import slices_from_str
from ._numpy import load_npz
from ._hdf5 import load_h5
import numpy as np
from collections import UserDict


class NDArraySpec(UserDict):
    class KEYS:
        PATH_FILE = 'path_file'
        PATH_DATASET = 'path_dataset'
        SLICES = 'slices'

    @property
    def path_file(self):
        return self.data.get(self.KEYS.PATH_FILE)

    @property
    def path_dataset(self):
        return self.data.get(self.KEYS.PATH_DATASET)

    @property
    def slices(self):
        return self.data.get(self.KEYS.SLICES)


def load_array(spec):
    path_file = spec.get('path_file')
    path_dataset = spec.get('path_dataset')
    slices = spec.get('slices')

    def maybe_slice(a):
        if slices is None:
            return a
        else:
            return a[slices_from_str(slices)]

    if path_file is None:
        raise TypeError("path_file not found in spec: {}.".format(spec))
    if path_file.endswith('.npy'):
        return maybe_slice(np.load(path_file))
    if path_file.endswith('.npz'):
        return maybe_slice(load_npz(path_file)[path_dataset])
    if path_file.endswith('.h5'):
        return load_h5(path_file, path_dataset, slices)
