from dxl.data.zoo.incident_position_estimation.dataclass import *
from dxl.data.function import (Take, OnIterator, To, head,
                               NestMapOf, AllIsInstance, GetAttr)
from pathlib import Path
import pytest
import numpy as np


@pytest.fixture
def photon_columns(path_of_db):
    return PhotonColumns(path_of_db)


def test_load_photon(photon_columns):
    photons = Take(10)(photon_columns)
    assert len(photons) == 10
    assert AllIsInstance(Photon)(photons)


def test_orm_to(photon_columns):
    orms_to_hits = GetAttr('hits') >> NestMapOf(ORMTo(Hit))
    load_one_photon = OnIterator(orms_to_hits) >> head
    hits = load_one_photon(photon_columns)
    assert isinstance(hits, list)
    assert AllIsInstance(Hit)(hits)


@pytest.fixture
def hits():
    return [
        Hit(0.0, 0.0, 0.0, 3.0),
        Hit(0.0, 0.0, 0.0, 1.0),
        Hit(0.0, 0.0, 0.0, 2.0),
    ]


def test_sort_hits_by_energy(hits):
    sorted_, first_index = sort_hits_by_energy(hits)
    assert first_index == 2
    assert len(sorted_) == 3


def test_random_shuffle_hits(hits):
    shuffled, first_index = random_shuffle_hits(hits)
    assert len(shuffled) == 3
    assert shuffled[first_index].e == 3.0


def test_load_photons_to_hits(photon_columns):
    orms_to_hits = (GetAttr('hits')
                    >> NestMapOf(ORMTo(Hit))
                    >> sort_hits_by_energy
                    >> To(ShuffledHitsWithIndex))
    load_one_photon = OnIterator(orms_to_hits) >> head
    hits = load_one_photon(photon_columns)
    assert isinstance(hits, ShuffledHitsWithIndex)


def test_load_with_crystal_center(photon_columns):
    orms_to_hits = (GetAttr('hits')
                    >> NestMapOf(ORMTo(HitWithCrystalCenter))
                    >> just_add_index
                    >> To(ShuffledHitsWithIndex))
    hits_iterator = OnIterator(orms_to_hits)(photon_columns)
    Take(2)(hits_iterator)  # drop first two samples
    data = head(hits_iterator)
    np.testing.assert_array_almost_equal(data.hits[0][:3], data.hits[1][:3])


def test_load_without_crystal_center(photon_columns):
    orms_to_hits = (GetAttr('hits')
                    >> NestMapOf(ORMTo(Hit))
                    >> just_add_index
                    >> To(ShuffledHitsWithIndex))
    hits_iterator = OnIterator(orms_to_hits)(photon_columns)
    Take(2)(hits_iterator)  # drop first two samples
    data = head(hits_iterator)
    np.sum(np.abs(np.array(data.hits[1][:3])
                  - np.array(data.hits[2][:3]))) > 0.5


@pytest.fixture
def hit_columns(photon_columns):
    orms_to_hits = (GetAttr('hits')
                    >> NestMapOf(ORMTo(Hit))
                    >> just_add_index
                    >> To(ShuffledHitsWithIndex))
    return ShuffledHitsColumns(photon_columns, OnIterator(orms_to_hits))


def test_shuffled_hits_columns_columns(hit_columns):
    assert hit_columns.columns == ('hits', 'first_hit_index')


def test_shuffled_hits_columns_dtypes(hit_columns):
    assert hit_columns.dtypes == {'hits': np.float32,
                                  'first_hit_index': np.int32}


def test_shuffled_hits_columns_shapes(hit_columns):
    expected_capacity = 16172
    assert hit_columns.shapes == {'hits': [expected_capacity, None, 4],
                                  'first_hit_index': [expected_capacity]}