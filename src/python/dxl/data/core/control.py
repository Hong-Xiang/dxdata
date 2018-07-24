from abc import ABCMeta, abstractmethod, abstractclassmethod
from typing import Callable, Union, List, Tuple, Dict, Generic, Callable, TypeVar
import collections.abc
from functools import singledispatch, partial

__all__ = ['Functor', 'fmap', 'Applicative', 'Monad']

a, b, c = TypeVar('a'), TypeVar('b'), TypeVar('c')


class Functor(Generic[a]):
    def __init__(self, data):
        self.data = data

    def fmap(self, f: Callable[[a], b]) -> 'Functor[b]':
        """
        Returns TypeOfFunctor(f(self.data)),
        mimics fmap :: (a -> b) -> a -> b by
        fmap( fa ) -> type(fmap)(f(a))
        """
        return Functor(f(self.data))


@singledispatch
def _fmap(fct, f):
    raise TypeError(
        f"Can't {type(f)} is not Functor or built-in Functor likes.")


@_fmap.register(Functor)
def _(fct, f):
    return fct.fmap(f)


@_fmap.register(list)
def _(xs, f):
    return [f(x) for x in xs]


@_fmap.register(tuple)
def _(xs, f):
    return tuple([f(x) for x in xs])


@_fmap.register(dict)
def _(dct, f):
    return {k: f(v) for k, v in dct.items()}


FunctorB = Union[List, Tuple, Dict, Functor[a]]


def fmap(f: Callable, fct: FunctorB) -> FunctorB:
    return _fmap(fct, f)


class Applicative(Functor[a]):
    def __init__(self, f):
        self.f = f

    def fmap(self, f):
        return Applicative(f(self.f))

    def apply(self, x: Functor[a]) -> Functor[b]:
        return self.fmap(lambda f: x.fmap(lambda x_: partial(f, x_)))

    def run(self) -> a:
        return self.fmap(lambda f: f())


class Monad(Applicative[a]):
    @abstractmethod
    def __rshift__(self, f):
        return self.fmap(f)
