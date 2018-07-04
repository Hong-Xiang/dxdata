from dxl.data.zoo.incident.data import (Photon, Hit, PhotonColumns, pytable_class)
def test_pytable_class():
    p = Photon([
        [Hit(0.0, 0.0, 0.0, 0.0) for _ in range(3)]
    ])
    c = pytable_class(p)
    assert len(c.columns) == 1

