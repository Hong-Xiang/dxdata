from dxl.shape import Box
import numpy as np

__all__ = ['ScannerSpec', 'CrystalID1', 'CrystalID2', 'CrystalID3']


class ScannerSpec:
    def __init__(self, inner_radius, nb_rings, nb_detectors_per_ring,
                 nb_blocks, ring_distance):
        self.inner_radius = inner_radius
        self.nb_rings = nb_rings
        self.nb_blocks = nb_blocks
        self.nb_detectors_per_ring = nb_detectors_per_ring
        self.ring_distance = ring_distance

    def index_dims(self):
        return (self.nb_blocks, self.nb_detectors_per_ring // self.nb_blocks,
                self.nb_rings)


class CrystalID1:
    def __init__(self, id):
        self.id = id

    def to(self, cls, spec):
        if cls == CrystalID3:
            x, y, z = np.unravel_index([self.id], spec.index_dims())
            return CrystalID3(x[0], y[0], z[0])
        else:
            return self.to(CrystalID3, spec).to(cls, spec)
        raise TypeError("Can not convert to {}".format(cls))

    def __eq__(self, c):
        if isinstance(c, CrystalID1) and self.id == c.id:
            return True
        return False

    def __repr__(self):
        return "<CrystalID1(id={})>".format(self.id)


class CrystalID2:
    def __init__(self, crystal_id, block_id):
        self.crystal_id = crystal_id
        self.block_id = block_id

    def to(self, cls, spec):
        if cls == CrystalID3:
            y, z = np.unravel_index([self.crystal_id], spec.index_dims()[1:])
            return CrystalID3(self.block_id, y[0], z[0])
        else:
            return self.to(CrystalID3, spec).to(cls, spec)
        raise TypeError("Can not convert to {}".format(cls))

    def __eq__(self, c):
        if isinstance(
                c, CrystalID2
        ) and self.crystal_id == c.crystal_id and self.block_id == c.block_id:
            return True
        return False

    def __repr__(self):
        return "<CrystalID2(crystal_id={}, block_id={})>".format(
            self.crystal_id, self.block_id)


class CrystalID3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def to(self, cls, spec: ScannerSpec):

        if cls == CrystalID1:
            return CrystalID1(
                np.ravel_multi_index([[self.x], [self.y], [self.z]],
                                     spec.index_dims())[0])
        if cls == CrystalID2:
            return CrystalID2(
                np.ravel_multi_index([[self.y], [self.z]],
                                     spec.index_dims()[:2])[0], self.x)
        raise TypeError("Can not convert to {}".format(cls))

    def __eq__(self, c):
        if isinstance(c, CrystalID3) and [self.x, self.y, self.z
                                          ] == [c.x, c.y, c.z]:
            return True
        return False

    def __repr__(self):
        return "<CrystalID3(x={}, y={}, z={})>".format(self.x, self.y, self.z)


class CrystalFactory:
    def __init__(self, spec: ScannerSpec):
        self.spec = spec

    def create(self, crystal_id):
        pass


class Crystal(Box):
    def __init__(self, size, center, normal, id):
        super().__init__(size, center, normal)
