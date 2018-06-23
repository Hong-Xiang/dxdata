from .core import Function

__all__ = ['NestMapOf']


class NestMapOf(Function):
    def __init__(self, f):
        self.f = f

    def __call__(self, x):
        return utils.nest.map(self.f, x)