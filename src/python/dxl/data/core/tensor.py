from .control import Functor
from collections.abc import Iterable
from abc import abstractproperty, ABC


class Tensor(Functor, ABC):
    @abstractproperty
    def data(self):
        pass

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


def is_tensor(t):
    if isinstance(t, Tensor):
        return True
