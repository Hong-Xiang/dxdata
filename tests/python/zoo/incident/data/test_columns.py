from dxl.data.zoo.incident.data import (
    PhotonColumns, QuerySpec, FeatureSpec, Photon, Coincidence)
from dxl.data.zoo.incident.function import database_load_all, database_loader


def test_construct(path_of_db):
    photons = database_load_all(database_loader.photon,
                                QuerySpec(path_of_db, 100, 100, 0),
                                FeatureSpec(None, True, True, None, None))
    pc = PhotonColumns(photons)
    assert pc.capacity == 100
    assert isinstance(pc[0], Photon)
