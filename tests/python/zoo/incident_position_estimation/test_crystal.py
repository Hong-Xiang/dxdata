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
    assert id1 == CrystalID3(1, 1, 0)


def test_223_2(spec):
    id0 = CrystalID2(10, 4)
    id1 = id0.to(CrystalID3, spec)
    assert id1 == CrystalID3(4, 1, 0)


def test_322(spec):
    id0 = CrystalID3(4, 1, 0)
    assert id0.to(CrystalID2, spec) == CrystalID2(10, 4)


def test_22122(spec):
    cid, bid = 10, 4
    id0 = CrystalID2(cid, bid)
    id1 = id0.to(CrystalID1, spec).to(CrystalID2, spec)
    assert id0 == id1


def test_create(spec):
    f = CrystalFactory(spec)
    c = f.create(CrystalID2(0, 0))
    assert (c.entity.origin() - Vector3(
        [spec.inner_radius, 0.0, -spec.height() / 2])).norm() < 1e-5
