from .core import Function, function

__all__ = [
    'head_arg', 'HeadNArgs', 'MultiMethodsFunction',
    'MultiMethodsByTypeOfFirstArg', 'MultiMethodsByFirstArg',
    'GetAttr'
]


@function
def head_arg(*args, **kwargs):
    return args[0]


class HeadNArgs(Function):
    def __init__(self, n):
        self.n = n

    def __call__(self, *args, **kwargs):
        return args[:self.n]


class MultiMethodsFunction(Function):
    def __init__(self, impls, finder):
        self.impls = impls
        self.finder = finder

    def __call__(self, *args, **kwargs):
        key = self.finder(*args, **kwargs)
        if self.impls.get(key) is None:
            raise NotImplementedError(
                "Not implementation of {} for {}.".format(type(self), key))
        return self.impls[key](*args, **kwargs)


class MultiMethodsByTypeOfFirstArg(MultiMethodsFunction):
    def __init__(self, impls):
        super().__init__(impls, self._finder)

    def _finder(self, *args, **kwargs):
        if type(args[0]) in self.impls:
            return type(args[0])
        for k in self.impls:
            if isinstance(k, type) and isinstance(args[0], k):
                return k
        return type(args[0])


class MultiMethodsByFirstArg(MultiMethodsFunction):
    def __init__(self, impls):
        super().__init__(impls, head_arg)


class GetAttr(Function):
    def __init__(self, name):
        self.name = name

    def __call__(self, x):
        return getattr(x, self.name)
