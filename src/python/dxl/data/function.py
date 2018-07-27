from dxl.data.control import Monad
from functools import partial
import inspect
from typing import Callable, Union, Generic

__all__ = ['Function']

from typing import TypeVar


a, b, c = TypeVar('a'), TypeVar('b'), TypeVar('c')


class Function(Monad[a], Generic[a, b]):
    def __init__(self, f, *, nargs=None):
        self.f = f
        if nargs is None:
            nargs = len(inspect.getfullargspec(f).args)
        self.nargs = nargs

    def __call__(self, *args, **kwargs) -> Union['Function[c, b]', b]:
        if len(args) < self.nargs:
            return Function(partial(self.f, *args, **kwargs))
        return self.f(*args, **kwargs)

    def bind(self, f: Callable[[b], c]) -> 'Function[a, c]':
        return self.fmap(f)

    def fmap(self, f: 'Function[b, c]') -> 'Function[a, c]':
        return Function(lambda *args, **kwargs: f(self.__call__(*args, **kwargs)))

    def __matmul__(self, f: 'Function[b, c]') -> 'Function[a, c]':
        def foo(*args):
            mid = f(*args[:f.nargs])
            return self(mid, *args[f.nargs:])
        return Function(foo, nargs=self.nargs - f.nargs + 1)

    # def __rshift__(self, f):
        # return Function(lambda *args, **kwargs: f(self.f(*args, **kwargs)), nargs=self.nargs-1)

    # def apply(self, x):
        # return Function(partial(self.__call__, x))
