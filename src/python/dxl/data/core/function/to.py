from .core import Function

__all__ = ['To']


class To(Function):
    def __init__(self, constructor):
        self.constructor = constructor

    def __call__(self, args=None, kwargs=None):
        args = args or ()
        kwargs = kwargs or {}
        return self.constructor(*args, **kwargs)
