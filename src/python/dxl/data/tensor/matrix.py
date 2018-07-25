from .tensor import Tensor


class Matrix(Tensor):
    def __init__(self, data):
        super().__init__(data)
        # if self.ndim != 2:
        # raise ValueError(f"Vector must be 1 dimensional, got {self.ndim}.")

    def fmap(self, f):
        return Matrix(f(self.data))

    def __matmul__(self, t):
        from dxl.function.tensor import ndim
        from .vector import Vector
        result = Tensor(self) @ Tensor(t)
        if isinstance(t, Vector):
            return Vector(result)
        if isinstance(t, Matrix):
            return Matrix(result)
        return Vector(result) if ndim(result) <= 1 else Matrix(result)

    def __rmatmaul__(self, t):
        return Matrix(Tensor(t) @ Tensor(self))
