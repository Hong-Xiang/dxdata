from typing import Sequence, TypeVar, Union, Callable
from collections import UserList
from dxl.data.control import Functor
from dxl.data.monoid import Monoid
import dask.bag as db

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

    def __add__(self, x: Union['List[a]', list]) -> 'List[a]':
        return type(self)(self.data + List(x).data)

    def fmap(self, f: Callable[[a], b]) -> 'List[b]':
        return type(self)([f(x) for x in self.data])
        # return type(self)(db.from_sequence(self.data).map(f))

    # def apply(self, x: 'List[a]') -> 'List[b]':
    #     # FIXME Applicative is not implemented yet, we may need to implement curry first.
    #     result = []
    #     for f in self.data:
    #         result += x.fmap(lambda x: partial(f, x))
    #     return List(result)
