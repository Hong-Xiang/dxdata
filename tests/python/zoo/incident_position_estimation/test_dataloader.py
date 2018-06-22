from dxl.data.zoo.incident_position_estimation import PhotonDataColumns
from pathlib import Path
import pytest


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


def test_load_normal(default_db):
    for i in range(10):
        print(next(default_db))