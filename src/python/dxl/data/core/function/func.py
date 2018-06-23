from .core import Function, function

__all__ = [
    'head_arg', 'HeadNArgs', 'MultiMethodsFunction',
    'MultiMethodsByTypeOfFirstArg', 'MultiMethodsByFirstArg'
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
        super().__init__(impls, head_arg >> type)


class MultiMethodsByFirstArg(MultiMethodsFunction):
    def __init__(self, impls):
        super().__init__(impls, head_arg)
