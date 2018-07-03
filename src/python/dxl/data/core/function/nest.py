from .core import Function, function
from .func import MultiMethodsByTypeOfFirstArg
from typing import NamedTuple
from collections import namedtuple

__all__ = ['NestMapOf', 'Take', 'head',
           'MapByNameOf', 'MapByPosition', 'append', 'Swap']


class NestMapOf(MultiMethodsByTypeOfFirstArg):
    def __init__(self, f):
        self.f = f
        super().__init__({
            list: self._impl_list,
            tuple: self._impl_tuple,
            dict: self._impl_dict,
        })

    def __call__(self, x):
        return super().__call__(x)

    def _impl_list(self, l):
        return [self.f(_) for _ in l]

    def _impl_dict(self, d):
        return {k: self.f(v) for k, v in d.items()}

    def _impl_tuple(self, t):
        return tuple([self.f(_) for _ in t])


class Take(Function):
    def __init__(self, n):
        self.n = n

    def __call__(self, it):
        return [x for _, x in zip(range(self.n), it)]


@function
def head(x):
    return Take(1)(x)[0]


class MapByNameOf(MultiMethodsByTypeOfFirstArg):
    def __init__(self, name, f):
        self.name = name
        self.f = f
        super().__init__({
            dict: self._impl_dict,
            NamedTuple: self._impl_named_tuple,
            namedtuple: self._impl_named_tuple,
            tuple: self._impl_named_tuple,
        })

    def __call__(self, x):
        return super().__call__(x)

    def _impl_dict(self, d):
        result = {}
        for k in d:
            if k == self.name:
                result[k] = self.f(d[k])
            else:
                result[k] = d[k]
        return result

    def _impl_named_tuple(self, t):
        result = [self.f(getattr(t, k))
                  if k == self.name
                  else getattr(t, k)
                  for k in t._fields]
        return type(t)(*result)


class MapByPosition(Function):
    def __init__(self, position, f):
        self.position = position
        self.f = f

    def __call__(self, x):
        return [self.f(_) if i == self.position else _ for i, _ in enumerate(x)]


@function
def append(l, x):
    return list(l) + [x]


class Swap(Function):
    def __init__(self, src, tar):
        self.src = src
        self.tar = tar

    def __call__(self, x):
        if self.src == self.tar:
            return x
        i_min, i_max = min(self.src, self.tar), max(self.src, self.tar)
        return (x[:i_min] + [x[i_max]]
                + x[i_min + 1: i_max]
                + [x[i_min]] + x[i_max + 1:])
