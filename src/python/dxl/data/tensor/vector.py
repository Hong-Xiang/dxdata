from .tensor import Tensor, T


class Vector(Tensor[T]):
    def __init__(self, data):
        super().__init__(data)
        if self.ndim != 1:
            raise ValueError(f"Vector must be 1 dimensional, got {self.ndim}.")

    def fmap(self, f):
        return Vector(f(self.data))

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def z(self):
        return self[2]
