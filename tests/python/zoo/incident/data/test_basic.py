import pytest
from dxl.data.zoo.incident.data.basic import *


class TestHit:
    def test_update(self):
        h0 = Hit(0.0, 0.0, 0.0, 0.0)
        h1 = h0.update(x=1.0)
        assert h1 is not h0
        assert h1.x == 1.0

    def test_repr(self):
        h = Hit(0.0, 1.0, 2.0, 3.0)
        assert str(h) == "<Hit(x=0.0, y=1.0, z=2.0, e=3.0)>"


class TestPhoton:
    def test_construct(self):
        p = Photon([Hit(0.0, 0.0, 0.0, 0.0),
                    Hit(0.0, 0.0, 0.0, 0.0)])

    def test_construct2(self):
        p = Photon([Hit(0.0, 0.0, 0.0, 0.0),
                    Hit(0.0, 0.0, 0.0, 0.0)],
                   first_hit_index=0)

        assert p.first_hit_index == 0
