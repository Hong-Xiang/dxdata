from .control import Monad
from functools import partial

class Maybe(Monad):
    def __init__(self, x):
        self.x = x
    
    def __eq__(self, m):
        return isinstance(m, Maybe) and m.join() == self.join()

    def join(self):
        return self.x
    
    def fmap(self, f):
        if self.x is None:
            return Maybe(None)
        else:
            return Maybe(f(self.x))
        
    def apply(self, v):
        return self.fmap(lambda f: partial(f, v))
    
    def __rshift__(self, f):
        return self.fmap(lambda x: f(x).join())

