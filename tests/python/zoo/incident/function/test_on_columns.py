from dxl.data.zoo.incident.data import PhotonColumns, QuerySpec, FeatureSpec
from dxl.data.zoo.incident.function import (
    FilterPhotonByNbHits, database_load_all, database_loader)

import pytest

@pytest.mark.skip("slow")
def test_filter_photon_by_nb_hits(query_spec):
    photons = database_load_all(database_loader.photon, query_spec,
                                FeatureSpec(None, True, True, None, None))
    pc0 = PhotonColumns(photons)
    pc1 = FilterPhotonByNbHits(2)(pc0)
    assert pc0.capacity == 611
    assert pc1.capacity == 176
    assert all(list(map(lambda x: len(x.hits)==2, iter(pc1))))

