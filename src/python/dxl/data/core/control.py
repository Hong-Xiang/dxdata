from abc import ABCMeta, abstractmethod, abstractclassmethod
from typing import Callable, Union, List, Tuple, Dict, Generic, Callable, TypeVar
import collections.abc
from functools import singledispatch

__all__ = ['Functor', 'fmap', 'Applicative', 'Monad']

a, b, c = TypeVar('a'), TypeVar('b'), TypeVar('c')


class Functor(Generic[a]):
    @abstractmethod
    def fmap(self, f: Callable[[a], b]) -> 'Functor[b]':
        """
        Returns TypeOfFunctor(f(self.data)),
        mimics fmap :: (a -> b) -> a -> b by
        fmap( fa ) -> type(fmap)(f(a))
        """
        pass


@singledispatch
def _fmap(fct, f):
    pass


FunctorB = Union[List, Tuple, Dict, Functor[a]]


def fmap(f: Callable, fct: FunctorB, *, lazy=False) -> FunctorB:
    if isinstance(fct, Functor):
        return fct.fmap(f, lazy=lazy)
    if isinstance(fct, (list, tuple)):
        return type(fct)(map(f, fct))
    if isinstance(fct, dict):
        return {k: f(v) for k, v in fct.items()}


class Applicative(Functor[a]):
    @abstractmethod
    def apply(self, x: Functor[a]) -> Functor[b]:
        pass

    @abstractclassmethod
    def lift2(self, fa: Functor[Callable[[a, b], c]]) -> 'Applicative[Callable[[a], b]]':
        ...

    def run(self) -> a:
        return self.fmap(lambda f: f())


class Monad(Applicative[a]):
    @abstractmethod
    def __rshift__(self, f):
        pass
