from abc import ABCMeta, abstractmethod, abstractclassmethod
from typing import Callable, Union, List, Tuple, Dict, Generic, Callable, TypeVar
import collections.abc
from functools import singledispatch, partial

__all__ = ['Functor', 'Applicative', 'Monad', 'SingleFunctor']

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


class SingleFunctor(Functor[Functor[a]]):
    def __init__(self, data: Functor[b]):
        self.data = data

    def fmap(self, f: Callable[[b], c]):
        return SimpleWrap(self.data.fmap(f))

    def join_to(self, type_):
        raise NotImplementedError

    def join(self):
        return self.data


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
    def __rshift__(self, f: Callable[[a], b]) -> 'Monad[b]':
        """ Alias to bind """
        return self.bind(f)

    @abstractmethod
    def bind(self, f: Callable[[a], b]) -> 'Monad[b]':
        return self.fmap(f)
