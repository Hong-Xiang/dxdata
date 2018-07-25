from abc import ABC, abstractproperty
from dxl.data.control import Functor
from typing import Generic, TypeVar, Callable
import operator

a, b, c = TypeVar('a'), TypeVar('b'), TypeVar('c')


class Pair(Functor[a], Generic[a, b]):
    """
    Base class with two elements.
    """

    def __init__(self, fst: a, snd: b):
        self.fst = fst
        self.snd = snd

    def fmap(self, f: Callable[[a], c]) -> 'Pair[c, b]':
        return Pair(f(self.fst), self.snd)

    def fmap2(self, f: Callable[[a], c]) -> 'Pair[c, c]':
        return self.fmap(f).flip().fmap(f).flip()

    def reduce(self, f: Callable[[a, a], b]) -> b:
        return f(self.snd, self.fst)

    def flip(self) -> 'Pair[b, a]':
        return Pair(self.snd, self.fst)

    def __repr__(self) -> str:
        return f"<Pair({self.fst}, {self.snd})>"
