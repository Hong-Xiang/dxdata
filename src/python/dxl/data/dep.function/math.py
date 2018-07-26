from dxl.data.function import Function


class LinearInterp(Function):
    def __init__(self, ratio):
        self.ratio = ratio

    def __call__(self, x, y):
        return [r * x + (1 - r) * y for r, x, y in zip(self.ratio, x, y)]
