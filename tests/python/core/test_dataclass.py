from dxl.data.core.dataclass import DataClass
import pytest


@pytest.fixture
def box():
    class Box(DataClass):
        __slots__ = ('origin', 'normal', 'shape')

        def __init__(self, origin, normal, shape):
            self.origin = origin
            self.normal = normal
            self.shape = shape
    return Box(1, 2, 3)


def test_replace(box):
    assert box.replace(origin=2).origin == 2


def test_fields(box):
    assert box.fields() == ('origin', 'normal', 'shape')
