from dxl.data.control import Monad
from typing import TypeVar, Callable

a, b = TypeVar('a'), TypeVar('b')


class IO(Monad[a]):
    def fmap(self, f: Callable[[a], b]) -> 'IO[b]':
        return f(self.data)
