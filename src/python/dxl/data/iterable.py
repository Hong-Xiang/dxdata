from typing import Iterable
from .control import Functor

__all__ = ['RestrictIterable', 'ChainableIterable', 'ItertoolsIterable']


class RestrictIterable(Iterable, Functor[Iterable]):
    """
    Only iterable, iterator is not RestrictIterable
    """


class ChainableIterable(RestrictIterable, Functor[Iterable]):
    def __init__(self, source: RestrictIterable, opeartion=None):
        from dxl.function import identity
        self.source = source
        if opeartion is None:
            opeartion = identity
        self.opeartion = opeartion

    def fmap(self, f):
        return ChainableIterable(self, f)

    def __iter__(self):
        return (self.opeartion(x) for x in self.source)


class ItertoolsIterable(RestrictIterable, Functor[Iterable]):
    def __init__(self, source: RestrictIterable, opeartion=None):
        self.source = source
        self.opeartion = opeartion

    def fmap(self, f):
        return ItertoolsIterable(self, f)

    def __iter__(self):
        return (x for x in self.opeartion(self.source))


import itertools


class Count(RestrictIterable):
    def __init__(self, start=0, step=1):
        self.start = start
        self.step = step

    def __iter__(self):
        return itertools.count(self.start, self.step)
