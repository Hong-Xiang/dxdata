from .tensor import Tensor, T


class Vector(Tensor[T]):
    def __init__(self, data):
        super().__init__(data)
        # if self.ndim > 1:
        # raise ValueError(f"Vector must be 1 dimensional or scalar, got {self.ndim}.")

    def fmap(self, f):
        return Vector(f(self.data))

    def __matmul__(self, t):
        from .matrix import Matrix
        result = Tensor(self) @ Tensor(t)
        if isinstance(t, Vector):
            return result
        return Matrix(result)

    def __rmatmul__(self, t):
        from .matrix import Matrix
        result = Tensor(t) @ Tensor(self)
        if isinstance(t, Vector):
            return result
        return Vector(result)

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def z(self):
        return self[2]
