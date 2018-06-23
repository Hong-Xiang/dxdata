from .core import Function, function

__all__ = ['AddBy']

class AddBy(Function):
    def __init__(self, value):
        self.value = value

    def __call__(self, x):
        return x + self.value
