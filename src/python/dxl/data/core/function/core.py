from functools import wraps
from dxl.data import utils

__all__ = [
    'Function', 'WrappedFunction', 'function', 'ChainedFunction', 'identity',
    'OnIterator', 'x'
]

from contextlib import contextmanager


class CallContext:
    def __init__(self, f, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.f = f
        self.prev = None

    def __enter__(self):
        self.prev = self.f._call_ctx()


class Function:
    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    def __rshift__(self, f):
        return ChainedFunction(self, f)

    def _call_ctx(self):
        pass


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


class LambdaMaker:
    def __getattr__(self, *args, **kwargs):
        return function(lambda _: getattr(_, *args, **kwargs))

    def __getitem__(self, *args, **kwargs):
        return function(lambda _: _.__getitem__(*args, **kwargs))


x = LambdaMaker()

# class MultiDispatchByFirstArg(MultiDispatchByArgs):
#     def __init__(self, implements):
#         super().__init__(implements, 1)
