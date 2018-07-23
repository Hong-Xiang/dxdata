from abc import ABC, abstractmethod, abstractclassmethod
from typing import Generic, TypeVar, Iterable, Sequence
import functools
import operator

__all__ = ['Semigroup', 'Monoid']

a = TypeVar('a')


class Semigroup(Generic[a], ABC):
    @abstractmethod
    def assosiative_operation(self, x: a) -> a:
        pass


class Monoid(Semigroup[a], ABC):
    @abstractclassmethod
    def empty(self) -> a:
        pass

    @classmethod
    def concat(cls, xss: Sequence[a]) -> a:
        acc = cls.empty()
        for xs in xss:
            for x in xs:
                acc = acc.append(x)
        return acc

    def assosiative_operation(self, x: a) -> 'Monoid[a]':
        return self.mappend(x)

    def mappend(self, x: a) -> 'Monoid[a]':
        return self.assosiative_operation(x)
