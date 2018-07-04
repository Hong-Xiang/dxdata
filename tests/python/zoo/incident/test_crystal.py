from dxl.data.zoo.incident.database.crystal import (
    CrystalID1, CrystalID2, CrystalID3, ScannerSpec, Crystal, CrystalFactory)
from dxl.shape import Vector3
import pytest
import json


def test_12221(scanner_spec):
    uid = 30
    id0 = CrystalID1(uid)
    id1 = CrystalID1(uid).to(CrystalID2, scanner_spec).to(CrystalID1, scanner_spec)
    assert id0 == id1


def test_123(scanner_spec):
    uid = 30
    id0 = CrystalID1(uid)
    id1 = CrystalID1(uid).to(CrystalID3, scanner_spec)
    assert id1 == CrystalID3(0, 3, 0)


def test_223(scanner_spec):
    id0 = CrystalID2(10, 1)
    id1 = id0.to(CrystalID3, scanner_spec)
    assert id1 == CrystalID3(1, 0, 1)


def test_223_2(scanner_spec):
    id0 = CrystalID2(10, 4)
    id1 = id0.to(CrystalID3, scanner_spec)
    assert id1 == CrystalID3(4, 0, 1)


def test_223_3(scanner_spec):
    id0 = CrystalID2(93, 4)
    id1 = id0.to(CrystalID3, scanner_spec)
    assert id1 == CrystalID3(4, 3, 9)


def test_322(scanner_spec):
    id0 = CrystalID3(4, 0, 1)
    assert id0.to(CrystalID2, scanner_spec) == CrystalID2(10, 4)


def test_322_2(scanner_spec):
    id0 = CrystalID3(4, 3, 9)
    id1 = id0.to(CrystalID2, scanner_spec)
    assert id1 == CrystalID2(93, 4)


def test_22122(scanner_spec):
    cid, bid = 10, 4
    id0 = CrystalID2(cid, bid)
    id1 = id0.to(CrystalID1, scanner_spec).to(CrystalID2, scanner_spec)
    assert id0 == id1


def test_create(scanner_spec):
    f = CrystalFactory(scanner_spec)
    c = f.create(CrystalID2(0, 0))
    assert (
        c.entity.origin() - Vector3([66.395, -15.03, -15.03])).norm() < 1e-5


def test_all_hit_in(scanner_spec):
    import pandas as pd
    from dxl.shape import Point
    data = pd.read_csv(
        '/mnt/gluster/CustomerTests/IncidentEstimation/SQLAlchemyDemo/simu0.1/hitsM.csv'
    )
    result = []
    f = CrystalFactory(scanner_spec)
    for i in range(100):
        row = data.iloc[i]
        c = f.create(CrystalID2(int(row['crystalID']), int(row['blockID'])))
        p = Point([row['posX'], row['posY'], row['posZ']])
        result.append(p.is_in(c.entity))
    assert all(result)
