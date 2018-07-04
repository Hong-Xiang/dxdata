from dxl.data.zoo.incident.database.query import *
from dxl.data.zoo.incident.database.orm import *
from dxl.data.function import identity


def test_nb_hits(path_of_db):
    assert nb.hits(path_of_db) == 1000


def test_nb_photon(path_of_db):
    assert nb.photon(path_of_db) == 611


def test_nb_coincidence(path_of_db):
    assert nb.coincidence(path_of_db) == 55


def test_single_photon(path_of_db):
    p = single.photon(path_of_db, identity)
    assert isinstance(p, Photon)
