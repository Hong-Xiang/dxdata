from dxl.data.function import Function, function, OnIterator, Filter
from ..data import PhotonColumns, CoincidenceColumns

__all__ = ['FilterPhotonByNbHits', 'FilterCoincidenceByNbHits',
           'FilterCoincidenceByNbPhoton']


class FilterPhotonByNbHits(Function):
    def __init__(self, nb_hits):
        self.nb_hits = nb_hits

    def __call__(self, columns: PhotonColumns):
        return PhotonColumns([p for p in columns.data
                              if len(p.hits) == self.nb_hits])


class FilterCoincidenceByNbHits(Function):
    def __init__(self, nb_hits, index_of_photon=1):
        self.index_of_photon = index_of_photon
        self.nb_hits = nb_hits

    def __call__(self, columns: CoincidenceColumns):
        return CoincidenceColumns([c for c in columns.data
                                   if len(c.photons[self.index_of_photon].hits) == self.nb_hits])


class FilterCoincidenceByNbPhoton(Function):
    def __init__(self, nb_photons=2):
        self.nb_photons = nb_photons

    def __call__(self, columns: CoincidenceColumns):
        return CoincidenceColumns([c for c in columns.data if len(c.photons) == self.nb_photons])
