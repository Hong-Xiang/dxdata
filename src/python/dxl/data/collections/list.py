from typing import Sequence, TypeVar, Union, Callable
from collections import UserList
from dxl.data.control import Functor
from dxl.data.monoid import Monoid
import dask.bag as db

a, b = TypeVar('a'), TypeVar('b')

__all__ = ['List', 'LazyList']


class List(UserList, Sequence[a], Functor[a], Monoid[a]):
    @classmethod
    def empty(self) -> 'List':
        return List([])

    def __getitem__(self, x) -> Union[a, 'List[a]', 'NoReturn']:
        if isinstance(x, int):
            return self.join()[x]
        if isinstance(x, slice):
            return type(self)(self.join()[x])
        raise TypeError(
            f"List indices must be integers or slices, not {type(x)}")

    def __add__(self, x: Union['List[a]', list]) -> 'List[a]':
        return type(self)(self.join() + List(x).join())

    def join(self):
        return self.data

    def fmap(self, f: Callable[[a], b]) -> 'List[b]':
        return type(self)([f(x) for x in self.join()])

    def head(self):
        return self.join()

    def tail(self):
        return self.fmap(lambda xs: xs[1:])

    # def apply(self, x: 'List[a]') -> 'List[b]':
    #     # FIXME Applicative is not implemented yet, we may need to implement curry first.
    #     result = []
    #     for f in self.data:
    #         result += x.fmap(lambda x: partial(f, x))
    #     return List(result)


import itertools


class LazyList(Functor[a], Monoid[a]):
    def __init__(self, iterable):
        if isinstance(iterable, LazyList):
            iterable = iterable.join()
        self.iterable = iterable

    @classmethod
    def empty():
        raise StopIteration

    def __iter__(self):
        return iter(self.join())

    def __add__(self, x):
        return self.fmap(lambda it: itertools.chain(it, x.join()))
