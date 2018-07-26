from dxl.data.control import Functor
from abc import ABC, abstractmethod


class Lazy(ABC, Functor):
    def __init__(self, expr):
        self.expr = expr

    @abstractmethod
    def join(self):
        pass
    
    def fmap(self, f, *, lazy=False):
        def result():
            return f(self.join())
        return LazyFunc(result)

class LazyFunc(Lazy):
    def join(self):
        return self.expr()
