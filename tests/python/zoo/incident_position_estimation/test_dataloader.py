from dxl.data.zoo.incident_position_estimation import PhotonDataColumns
from pathlib import Path
import pytest
import numpy as np


@pytest.fixture
def default_db(path_of_db):
    return PhotonDataColumns(path_of_db)


def test_load(default_db):
    s = next(default_db)
    assert s['hits'].shape == (1, 4)
    assert isinstance(s['first_hit'], int)


def test_load_multiple(default_db):
    first_hits = set()
    for i in range(10):
        s = next(default_db)
        assert s['hits'].shape[1] == 4
        first_hits.add(s['first_hit'])
    assert len(first_hits) > 1


def test_load_with_crystal_center(path_of_db):
    dcs = PhotonDataColumns(
        path_of_db, is_crystal_center=True, is_shuffle=False)
    for i in range(2):
        next(dcs)
    data = next(dcs)
    np.testing.assert_array_almost_equal(data['hits'][0][:3],
                                         data['hits'][1][:3])


def test_load_without_crystal_center(path_of_db):
    dcs = PhotonDataColumns(path_of_db, is_crystal_center=False)
    for i in range(2):
        next(dcs)
    data = next(dcs)
    assert np.sum(np.abs(data['hits'][1][:3] - data['hits'][2][:3])) > 0.5
