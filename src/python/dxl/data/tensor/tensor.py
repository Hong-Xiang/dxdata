from dxl.data import Functor
from collections.abc import Iterable
from abc import abstractproperty, ABC
import numpy as np
from typing import TypeVar
import functools
import operator

T = TypeVar('TensorLike')


class Tensor(Functor[T]):
    def __init__(self, data):
        from dxl.function.tensor import to_tensor_like
        self.data = to_tensor_like(data)

    def join(self):
        """
        Return un-wrapped raw tensor.
        """
        return self.data

    @property
    def shape(self):
        from dxl.function.tensor import shape
        return shape(self.data)

    @property
    def ndim(self):
        from dxl.function.tensor import ndim
        return ndim(self.data)

    @property
    def size(self):
        return functools.reduce(operator.mul, self.shape, 1)

    def __getitem__(self, s):
        return self.fmap(lambda d: d[s])

    def __iter__(self):
        return self.fmap(iter)

    def fmap(self, f):
        return Tensor(f(self.data))

    def __eq__(self, t):
        return self.fmap(lambda d: d == t)

    def __req__(self, t):
        return self.fmap(lambda d: t == d)

    def __mul__(self, t):
        return self.fmap(lambda d: d * t)

    def __rmul__(self, t):
        return self.fmap(lambda d: t * d)

    def __matmul__(self, t):
        return self.fmap(lambda d: d @ m)

    def __rmatmaul__(self, t):
        return self.fmap(lambda d: m@d)

    def __add__(self, t):
        return self.fmap(lambda d: d + x)

    def __radd__(self, t):
        return self.fmap(lambda d: x + d)

    def __sub__(self, t):
        return self.fmap(lambda d: d - t)

    def __rsub__(self, t):
        return self.fmap(lambda d: t - d)

    def __truediv__(self, t):
        return self.fmap(lambda d: d / t)

    def __rtruediv__(self, t):
        return self.fmap(lambda d: t / d)

    def __floordiv__(self, t):
        return self.fmap(lambda d: d // t)

    def __floordiv__(self, t):
        return self.fmap(lambda d: t // d)

    def __mod__(self, t):
        return self.fmap(lambda d: d % t)

    def __rmod__(self, t):
        return self.fmap(lambda d: t % d)

    def __repr__(self):
        return repr(self.data)
