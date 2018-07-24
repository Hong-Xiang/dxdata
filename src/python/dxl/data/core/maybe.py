from typing import Generic, TypeVar
from .control import Monad, Monoid

a = TypeVar('a')

class Maybe(Generic[a]):
    def __init__(self, data=None):
        self.data = data
    
    
