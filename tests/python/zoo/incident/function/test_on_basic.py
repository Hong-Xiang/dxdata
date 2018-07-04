from dxl.data.zoo.incident.data import *
from dxl.data.zoo.incident.function import (
    random_shuffle_hits, just_add_index, sort_hits_by_energy)

from dxl.data.function import mono_increase, x

import pytest


@pytest.fixture
def photon():
    return Photon([
        Hit(43.40, 50.49, -15.30, 0.05),
        Hit(43.40, 50.49, -15.30, 0.07),
        Hit(43.40, 50.49, -15.30, 0.06),
    ])


@pytest.fixture
def coincidence(photon):
    return Coincidence([
        photon,
        Photon([
            Hit(-66.39, -8.34, -1.67, 0.012),
            Hit(-66.39, -8.34, -1.67, 0.19),
        ])
    ])


def test_sort_hits_by_energy(photon):
    p = sort_hits_by_energy(photon)
    assert p is not photon
    assert len(p.hits) == 3
    assert p.first_hit_index == 0
    assert mono_increase(list(map(x.e, p.hits)))
