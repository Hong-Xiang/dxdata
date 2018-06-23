from .core import Function

__all__ = ['To']


class To(Function):
    def __init__(self, constructor):
        self.constructor = constructor

    def __call__(self, *args, **kwargs):
        return self.constructor(*args, **kwargs)
