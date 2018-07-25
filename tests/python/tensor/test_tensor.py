from dxl.data.tensor import Tensor
from dxl.function.tensor import all_close


def test_add():
    a, b = Tensor([1, 2]), Tensor([3, 4])
    c = Tensor([4, 6])
    assert all_close(a + b, c)
