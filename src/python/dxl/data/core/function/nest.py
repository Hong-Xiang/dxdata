from .core import Function

__all__ = ['NestMapOf', 'Take', 'Head']


class NestMapOf(Function):
    def __init__(self, f):
        self.f = f

    def __call__(self, x):
        return utils.nest.map(self.f, x)


class Take(Function):
    def __init__(self, n):
        self.n = n

    def __call__(self, it):
        return [x for _, x in zip(range(self.n), it)]


Head = Take(1)