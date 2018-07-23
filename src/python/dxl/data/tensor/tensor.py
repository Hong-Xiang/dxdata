from dxl.data import Functor
from collections.abc import Iterable
from abc import abstractproperty, ABC
import numpy as np


class Tensor(Functor):
    def __init__(self, data):
        self.data = data

    @property
    def shape(self):
        return list(self.data.shape)

    @property
    def ndim(self):
        return self.data.ndim

    def __getitem__(self, s):
        return self.data[s]

    def __iter__(self):
        if isinstance(self.data, Iterable):
            return iter(self.data)
        else:
            return (self.__getitem__[i, ...] for i in range(self.shape[0]))

    def fmap(self, f):
        from dxl.function.tensor import list2tensor, BatchableFunction
        if isinstance(f, BatchableFunction):
            return Tensor(f(self.data))
        else:
            return Tensor(list2tensor([f(x) for x in self.__iter__()]))

    def __eq__(self, t):
        if self.shape != list(t.shape):
            return False
        if isinstance(t, Tensor):
            t = t.data
        if isinstance(self.data, np.ndarray):
            return np.allclose(self.data, t)


def is_tensor(t):
    if isinstance(t, Tensor):
        return True
