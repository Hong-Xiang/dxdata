from abc import ABC, abstractmethod, abstractclassmethod
from typing import Generic, TypeVar, Iterable, Sequence
import functools
import operator

__all__ = ['Monoid']

a = TypeVar('a')


class Monoid(Generic[a]):
    @abstractclassmethod
    def empty(self) -> a:
        pass

    @classmethod
    def concat(cls, xss: Sequence[a]) -> a:
        return functools.reduce(operator.add, xss, cls.empty())

    @abstractmethod
    def __add__(self, x: a) -> 'Monoid[a]':
        pass
