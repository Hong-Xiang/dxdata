from .control import Monad
from functools import partial

from typing import TypeVar, Callable

a, b = TypeVar('a'), TypeVar('b')

class Maybe(Monad[a]):
    def __init__(self, data):
        self.data = data
    
    def __eq__(self, m):
        return isinstance(m, Maybe) and m.join() == self.join()

    def join(self) -> a:
        return self.data
    
    def fmap(self, f: Callable[[a], b]) -> 'Maybe[b]':
        if self.join() is None:
            return Maybe(None)
        else:
            return Maybe(f(self.join()))
        
    def apply(self, v):
        return self.fmap(lambda f: partial(f, v))
    
    def bind(self, f: Callable[[a], 'Maybe[b]']) -> 'Maybe[b]':
        return self.fmap(lambda x: f(x).join())

