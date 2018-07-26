from dxl.data.control import Monad

__all__ = ['Function']

from typing import TypeVar

a = TypeVar('a')


class Function(Monad[a]):
    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        return self.f(*args, **kwargs)

    def bind(self, f):
        return self.fmap(f)

    def fmap(self, f):
        return Function(lambda *args, **kwargs: f(self.__call__(*args, **kwargs)))

    # def apply(self, x):
        # return Function(partial(self.__call__, x))
