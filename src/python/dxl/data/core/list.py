from typing import Sequence, TypeVar, Union, Callable
from collections import UserList
from .control import Functor
from .monoid import Monoid

a, b = TypeVar('a'), TypeVar('b')

__all__ = ['List']


class List(UserList, Sequence[a], Functor[a], Monoid[a]):
    @classmethod
    def empty(self) -> 'List':
        return List([])

    def __getitem__(self, x) -> Union[a, 'List[a]', 'NoReturn']:
        if isinstance(x, int):
            return self.data[x]
        if isinstance(x, slice):
            return type(self)(self.data[x])
        raise TypeError(
            f"List indices must be integers or slices, not {type(x)}")

    def mappend(self, x: Union['List[a]', list]) -> 'List[a]':
        x = List(x)
        result_type = type(self) if self != self.empty() else type(x)
        return List(self.data + [x])

    def fmap(self, f: Callable[[a], b]) -> 'List[b]':
        return List([f(x) for x in self.data])

    @classmethod
    def concat(cls, xs: Sequence['List[a]']) -> 'List[a]':
        acc = cls.empty()
        for x in xs:
            acc += x
        return acc

    def apply(self, x: 'List[a]') -> 'List[b]':
        # FIXME Applicative is not implemented yet, we may need to implement curry first.
        result = []
        for f in self.data:
            result += x.fmap(lambda x: partial(f, x))
        return List(result)
