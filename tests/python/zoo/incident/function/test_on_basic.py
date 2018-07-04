from dxl.data.zoo.incident.data import Hit, Photon, Coincidence
from dxl.data.zoo.incident.function.on_basic import *

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


def test_padding_photon(photon):
    p = PaddingPhoton(5)(photon)
    assert p is not photon
    assert len(photon.hits) == 3
    assert len(p.hits) == 5


def test_swap_photon(coincidence):
    c = swap_photon(coincidence)
    assert c is not coincidence
    assert c.photons[0] is coincidence.photons[1]
    assert c.photons[1] is coincidence.photons[0]
