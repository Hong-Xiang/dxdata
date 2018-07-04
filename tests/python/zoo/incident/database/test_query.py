from dxl.data.zoo.incident.database.query import *
from dxl.data.zoo.incident.database.orm import *
from dxl.data.function import identity

def test_single_photon(path_of_db):
    p = single.photon(path_of_db, identity)
    assert isinstance(p, Photon)