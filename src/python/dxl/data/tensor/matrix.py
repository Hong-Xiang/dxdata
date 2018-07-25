from .tensor import Tensor


class Matrix(Tensor):
    def __init__(self, data):
        super().__init__(data)
        if self.ndim != 2:
            raise ValueError(f"Vector must be 1 dimensional, got {self.ndim}.")

    def fmap(self, f):
        return Vector(f(self.data))
