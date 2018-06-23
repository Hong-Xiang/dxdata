from functools import wraps
from dxl.data import utils

__all__ = [
    'Function', 'WrappedNormalFunction', 'function', 'ChainedFunction',
    'AddBy', 'NestMapOf', 'echo', 'Len', "MultiDispatchByArgs"
]


class Function:
    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    def __rshift__(self, f):
        return ChainedFunction(self, f)


class WrappedNormalFunction(Function):
    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        return self.f(*args, **kwargs)


def function(f):
    return WrappedNormalFunction(f)


class ChainedFunction(Function):
    def __init__(self, prev, succ):
        self.prev = prev
        self.succ = succ

    def __call__(self, *args, **kwargs):
        return self.succ(self.prev(*args, **kwargs))


class AddBy(Function):
    def __init__(self, value):
        self.value = value

    def __call__(self, x):
        return x + self.value


class NestMapOf(Function):
    def __init__(self, f):
        self.f = f

    def __call__(self, x):
        return utils.nest.map(self.f, x)


@function
def echo(x):
    return x


@function
def Len(x):
    return len(x)


class MultiDispatchByArgs(Function):
    def __init__(self, implements=None, len_of_key=None):
        if len_of_key is None:
            if implements is not None:
                key = list(implements.keys())[0]
                if isinstance(key, type):
                    len_of_key = 1
                else:
                    len_of_key = len(key)
            else:
                raise TypeError(
                    "Can not infer len_of_key with none explicit implements dict."
                )
        if implements is None:
            implements = {}
        self.implements = implements
        self.len_of_key = len_of_key

    def __call__(self, *args, **kwargs):
        key = tuple(map(lambda x: x.__class__, args[:self.len_of_key]))
        if len(key) == 1:
            key = key[0]
        func = self.implements.get(key)
        if func is None:
            func = getattr(self, sum('_{}'.format(c.__name__) for c in key))
        if func is None:
            raise NotImplementedError(
                "No implementation of {} for  {}.".format(self.__class__, key))
        return func(*args, **kwargs)
