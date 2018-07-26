from .control import Monad
from typing import Generic, TypeVar

a =  TypeVar('a')

class ContextManager(Monad[a], Generic[a]):
    def __irshift__(self, f):
        with self.__enter__() as scope:
            return f(scope)
