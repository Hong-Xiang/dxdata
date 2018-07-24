from typing import Generic, TypeVar, Callable
from .control import Monad, Monoid

a, b = TypeVar('a'), TypeVar('b')

class Maybe(Monad[a], Monoid[a]):
    def __init__(self, data=None):
        self.data = data
    
    def fmap(self, f):
        if self.data is None:
            return Maybe()
        else:
            return Maybe(f(self.data))
    
    def __rshift__(self, f: Callable[[a], 'Maybe[b]']) -> 'Maybe[b]':
        return self.fmap(f)

