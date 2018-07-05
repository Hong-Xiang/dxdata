import pytest
from dxl.data.zoo.incident.function import columns2pytable
from dxl.data.zoo.incident.data import PhotonColumns, FeatureSpec, Photon, Hit


def make_photon_columns(nb_photons):
    photons = [Photon(hits=[Hit(1.0, 1.0, 1.0, 1.0)
                            for _ in range(3)]) for _ in range(nb_photons)]
    return PhotonColumns(photons)


def test_create_table(tmpdir, query_spec):
    # p = str(tmpdir.mkdir('test_create_table').join('test.h5'))
    p = '/tmp/test/test.h5'
    columns2pytable(make_photon_columns(10), p)
    from tables import open_file
    with open_file(p, 'r') as fin:
        db = fin.root.data
        assert db.nrows == 10
