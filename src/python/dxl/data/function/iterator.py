from dxl.data.function import Function


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
