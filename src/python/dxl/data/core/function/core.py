from functools import wraps
from dxl.data import utils

__all__ = [
    'Function', 'WrappedFunction', 'function', 'ChainedFunction', 'identity',
    'OnIterator'
]


class Function:
    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    def __rshift__(self, f):
        return ChainedFunction(self, f)


class WrappedFunction(Function):
    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        return self.f(*args, **kwargs)


def function(f):
    return WrappedFunction(f)


class ChainedFunction(Function):
    def __init__(self, prev, succ):
        self.prev = prev
        self.succ = succ

    def __call__(self, *args, **kwargs):
        return self.succ(self.prev(*args, **kwargs))


identity = function(lambda _: _)


class OnIterator(Function):
    def __init__(self, f):
        self.f = f

    def __call__(self, it, *args, **kwargs):
        def result():
            for x in it:
                yield self.f(x, *args, **kwargs)

        return result()


# class MultiDispatchByFirstArg(MultiDispatchByArgs):
#     def __init__(self, implements):
#         super().__init__(implements, 1)
