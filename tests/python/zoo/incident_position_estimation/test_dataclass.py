from dxl.data.zoo.incident_position_estimation.data import *
from dxl.data.function import (Take, OnIterator, To, head,
                               NestMapOf, AllIsInstance, GetAttr,
                               MapWithUnpackArgsKwargs)
from pathlib import Path
import pytest
import numpy as np


@pytest.fixture
def photon_columns(path_of_db):
    return PhotonColumns(path_of_db, False, 1000, 1000)


@pytest.fixture
def hits_list_to_named_tuple():
    return MapWithUnpackArgsKwargs(To(ShuffledHitsWithIndex))


def test_load_photon(photon_columns):
    photons = Take(10)(photon_columns)
    assert len(photons) == 10
    assert AllIsInstance(Photon)(photons)


def test_orm_to(photon_columns):
    # orms_to_hits = GetAttr('hits') >> NestMapOf(ORMTo(Hit))
    # load_one_photon = OnIterator(orms_to_hits) >> head
    p = head(photon_columns)
    assert isinstance(p, Photon)
    assert isinstance(p.hits, list)
    assert AllIsInstance(Hit)(p.hits)


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


def test_load_photons_to_hits(photon_columns, hits_list_to_named_tuple):
    orms_to_hits = (GetAttr('hits')
                    >> sort_hits_by_energy
                    >> hits_list_to_named_tuple)
    load_one_photon = OnIterator(orms_to_hits) >> head
    hits = load_one_photon(photon_columns)
    assert isinstance(hits, ShuffledHitsWithIndex)


def test_load_with_crystal_center(path_of_db, hits_list_to_named_tuple):
    photon_columns = PhotonColumns(path_of_db, HitWithCrystalCenter)
    orms_to_hits = (GetAttr('hits')
                    >> just_add_index
                    >> hits_list_to_named_tuple)
    hits_iterator = OnIterator(orms_to_hits)(photon_columns)
    Take(2)(hits_iterator)  # drop first two samples
    data = head(hits_iterator)
    np.testing.assert_array_almost_equal(data.hits[0][:3], data.hits[1][:3])


def test_load_without_crystal_center(photon_columns, hits_list_to_named_tuple):
    orms_to_hits = (GetAttr('hits')
                    >> just_add_index
                    >> hits_list_to_named_tuple)
    hits_iterator = OnIterator(orms_to_hits)(photon_columns)
    Take(2)(hits_iterator)  # drop first two samples
    data = head(hits_iterator)
    np.sum(np.abs(np.array(data.hits[1][:3])
                  - np.array(data.hits[2][:3]))) > 0.5


@pytest.fixture
def hit_columns(photon_columns):
    photon2shuffled_hits = (GetAttr('hits')
                            >> just_add_index
                            >> hits_list_to_named_tuple)
    return ShuffledHitsColumns(photon_columns, ShuffledHitsWithIndex,
                               OnIterator(photon2shuffled_hits))


def test_shuffled_hits_columns_columns(hit_columns):
    assert hit_columns.columns == ('hits', 'first_hit_index')


def test_shuffled_hits_columns_dtypes(hit_columns):
    assert hit_columns.dtypes == {'hits': np.float32,
                                  'first_hit_index': np.int32}


def test_shuffled_hits_columns_shapes(hit_columns):
    expected_capacity = 16172
    assert hit_columns.shapes == {'hits': [expected_capacity, None, 4],
                                  'first_hit_index': [expected_capacity]}


def test_padded_hits_columns_0(path_of_db):
    columns = padded_hits_columns(path_of_db, 10, Hit, just_add_index, True)
    h = head(columns)
    assert isinstance(h, ShuffledHitsWithIndexAndPaddedSize)
    assert h.first_hit_index == 0
    assert h.padded_size == 9
    assert h.hits.shape == (10, 4)
    assert len(columns.shapes) == 3


def test_padded_hits_columns_1(path_of_db):
    columns = padded_hits_columns(path_of_db, 10, Hit, just_add_index, False)
    h = head(columns)
    assert isinstance(h, ShuffledHitsWithIndex)
    assert h.first_hit_index == 0
    assert h.hits.shape == (10, 4)
    assert len(columns.shapes) == 2
