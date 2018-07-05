from dxl.data.zoo.incident.function.on_db import *
from dxl.data.zoo.incident.data import FeatureSpec, Hit
from dxl.data.zoo.incident.database.query import single


def test_to_hit(path_of_db):
    fs = FeatureSpec(None, True, True, None, None)
    hit = single.hit(path_of_db, ToHit(fs))
    assert isinstance(hit, Hit)
    assert hit.crystal_index is not None
