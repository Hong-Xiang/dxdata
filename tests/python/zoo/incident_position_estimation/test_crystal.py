from dxl.data.zoo.incident_position_estimation import (
    CrystalID1, CrystalID2, CrystalID3, ScannerSpec, Crystal, CrystalFactory)
from dxl.shape import Vector3
import pytest
import json


@pytest.fixture
def spec(path_resource):
    with open(path_resource / 'PETSystems' / 'MindTracker' / 'block8' /
              'spec.json', 'r') as fin:
        return ScannerSpec(**json.load(fin))


def test_12221(spec):
    uid = 30
    id0 = CrystalID1(uid)
    id1 = CrystalID1(uid).to(CrystalID2, spec).to(CrystalID1, spec)
    assert id0 == id1


def test_123(spec):
    uid = 30
    id0 = CrystalID1(uid)
    id1 = CrystalID1(uid).to(CrystalID3, spec)
    assert id1 == CrystalID3(0, 3, 0)


def test_223(spec):
    id0 = CrystalID2(10, 1)
    id1 = id0.to(CrystalID3, spec)
    assert id1 == CrystalID3(1, 0, 1)


def test_223_2(spec):
    id0 = CrystalID2(10, 4)
    id1 = id0.to(CrystalID3, spec)
    assert id1 == CrystalID3(4, 0, 1)


def test_223_3(spec):
    id0 = CrystalID2(93, 4)
    id1 = id0.to(CrystalID3, spec)
    assert id1 == CrystalID3(4, 3, 9)


def test_322(spec):
    id0 = CrystalID3(4, 0, 1)
    assert id0.to(CrystalID2, spec) == CrystalID2(10, 4)


def test_322_2(spec):
    id0 = CrystalID3(4, 3, 9)
    id1 = id0.to(CrystalID2, spec)
    assert id1 == CrystalID2(93, 4)


def test_22122(spec):
    cid, bid = 10, 4
    id0 = CrystalID2(cid, bid)
    id1 = id0.to(CrystalID1, spec).to(CrystalID2, spec)
    assert id0 == id1


def test_create(spec):
    f = CrystalFactory(spec)
    c = f.create(CrystalID2(0, 0))
    assert (
        c.entity.origin() - Vector3([66.395, -15.03, -15.03])).norm() < 1e-5


def test_all_hit_in(spec):
    import pandas as pd
    from dxl.shape import Point
    data = pd.read_csv(
        '/mnt/gluster/CustomerTests/IncidentEstimation/SQLAlchemyDemo/simu0.1/hitsM.csv'
    )
    result = []
    f = CrystalFactory(spec)
    for i in range(100):
        row = data.iloc[i]
        c = f.create(CrystalID2(int(row['crystalID']), int(row['blockID'])))
        p = Point([row['posX'], row['posY'], row['posZ']])
        result.append(p.is_in(c.entity))
    assert all(result)
