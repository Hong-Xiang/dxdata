from dxl.data.zoo.incident_position_estimation.generate import (
    auto_flush, NB_CHUNK, Crystals)

import pytest
import numpy as np


@pytest.fixture
def session_spy():
    class SessionSpy:
        def __init__(self):
            self.flushed = 0
            self.objects = []

        def flush(self):
            self.flushed += 1

        def add(self, o):
            self.objects.append(o)

    return SessionSpy()


def test_auto_flush(session_spy):
    @auto_flush()
    def foo(session):
        pass

    assert session_spy.flushed == 0
    for i in range(NB_CHUNK):
        foo(session_spy)
    assert session_spy.flushed == 1
    for i in range(NB_CHUNK):
        foo(session_spy)
    assert session_spy.flushed == 2


class TestCrystal:
    def test_construct(self, scanner_spec):
        cs = Crystals(scanner_spec)
    
    def assertCrystalEqual(self, crystal, ids, position, shape, normal):
        if (crystal.crystal_id != ids[0]
            or crystal.block_id != ids[1]
            or np.testing.assert_array_almost_equal([
             crystal.x,
             crystal.y,
             crystal.z,
             crystal.width,
             crystal.height,
             crystal.depth,
             crystal.normal_x,
             crystal.normal_y,
             crystal.normal_z,
         ],position+shape+normal) 
        ):
            return False
        return True

    def test_make(self, scanner_spec, session_spy):
        cs = Crystals(scanner_spec)
        c = cs.make(session_spy, None, 0, 0)
        self.assertCrystalEqual(c, [0, 0], [66.395, -15.03, -15.03], [3.34, 3.34, 33.4], [1.0, 0.0, 0.0])