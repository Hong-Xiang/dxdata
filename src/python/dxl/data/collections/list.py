from collections import UserList
from dxl.data.control import Monad, Applicative, Functor, Monoid
from functools import partial

__all__ = ['List', 'ListFunc']


class List(UserList, Functor, Monoid):
    @classmethod
    def empty(self):
        return List([])

    def __getitem__(self, x):
        if isinstance(x, int):
            return self.data[x]
        if isinstance(x, slice):
            return type(self)(self.data[x])
        raise TypeError(
            f"List indices must be integers or slices, not {type(x)}")

    def __add__(self, x: 'List'):
        if isinstance(x, list):
            x = List(x)
        elif not isinstance(x, List):
            raise TypeError(f"Can't add {type(self)} with {type(x)}")
        result_type = type(self) if self != self.empty() else type(x)
        return result_type(self.data + x)

    def fmap(self, f):
        return type(self)([f(x) for x in self.data])
    
    @classmethod
    def concat(cls, xs):
        if isinstance(xs, list):
            xs = List(xs)
        result = cls.empty()
        for x in xs:
            result = result + x
        return result

class ListFunc(List, Applicative):
    def apply(self, x: 'List'):
        result = []
        for f in self.data:
            result += x.fmap(lambda x: partial(f, x))
        return ListFunc(result)
    
    @classmethod
    def from_(cls, xs):
        if isinstance(xs, List):
            return ListFunc(xs.data)
        if isinstance(xs, list):
            return ListFunc(xs)
        raise TypeError(f"Can't convert {type(x)} to ListFunc.")