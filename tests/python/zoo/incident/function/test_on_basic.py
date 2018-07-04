from dxl.data.zoo.incident.data import *
from dxl.data.zoo.incident.function import (coincidence2shuffled_hits,
                                                                sort_hits_by_energy, photon2shuffled_hits)

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


def test_photon2shuffled_hits(photon):
    sh = photon2shuffled_hits(5, sort_hits_by_energy)(photon)
    assert sh.hits.shape == (5, 4)
    assert sh.first_hit_index == 0
    assert sh.padded_size == 2


def test_coincidence2shuffled_hits(coincidence):
    sh = coincidence2shuffled_hits(5, sort_hits_by_energy)(coincidence)
    assert sh.hits.shape == (5, 8)
    assert sh.first_hit_index == 0
    assert sh.padded_size == 2
