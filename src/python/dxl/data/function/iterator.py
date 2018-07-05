from dxl.data.function import Function

__all__ = ['SelectPer', 'DropPer', 'ApplyAllOn', 'ApplyWith']


class SelectPer(Function):
    def __init__(self, period):
        self.period = period

    def __call__(self, inputs):
        def it():
            for i, x in enumerate(inputs):
                if i % self.period == 0:
                    yield x
        return it()


class DropPer(Function):
    def __init__(self, period):
        self.period = period

    def __call__(self, inputs):
        def it():
            for i, x in enumerate(inputs):
                if i % self.period != 0:
                    yield x
        return it()


class ApplyAllOn(Function):
    def __init__(self, target):
        self.target = target

    def __call__(self, funcs):
        return (f(self.target) for f in funcs)


class ApplyWith(Function):
    def __init__(self, funcs):
        self.funcs = funcs

    def __call__(self, target):
        return (f(target) for f in self.funcs)
