import pytest
from dxl.data.zoo.incident.function import columns2pytable
from dxl.data.zoo.incident.data import PhotonColumns, FeatureSpec, Photon, Hit, Coincidence, CoincidenceColumns


def make_photon(nb_hits=3):
    return Photon(hits=[Hit(0.0, 0.0, 0.0, 0.0) for _ in range(3)], first_hit_index=0)


def make_photons(nb_photons=10, nb_hits=3):
    return [make_photon(nb_hits) for _ in range(nb_photons)]


def make_coincidence(nb_hits=3):
    return Coincidence(make_photons(2, nb_hits))


def make_coincidence_columns(nb_coincidences, nb_hits=3):
    return CoincidenceColumns([make_coincidence(nb_hits) for _ in range(nb_coincidences)])


def test_create_table(tmpdir):
    p = str(tmpdir.mkdir('test_create_table').join('test.h5'))
    columns2pytable(PhotonColumns(make_photons(10)), p)
    from tables import open_file
    with open_file(p, 'r') as fin:
        db = fin.root.data
        assert db.nrows == 10


def test_create_coincidence_table(tmpdir):
    p = str(tmpdir.mkdir('test_create_table').join('test.h5'))
    columns2pytable(make_coincidence_columns(5), p)
    from tables import open_file
    with open_file(p, 'r') as fin:
        db = fin.root.data
        assert db.nrows == 5
