from dxl.shape import Box
import numpy as np
import json

__all__ = [
    'ScannerSpec', 'CrystalID1', 'CrystalID2', 'CrystalID3', 'Crystal',
    'CrystalFactory'
]


class ScannerSpec:
    def __init__(self, inner_diameter, nb_rings, nb_detectors_per_ring,
                 nb_blocks, ring_distance, crystal_length):
        self.inner_diameter = inner_diameter
        self.nb_rings = nb_rings
        self.nb_blocks = nb_blocks
        self.nb_detectors_per_ring = nb_detectors_per_ring
        self.ring_distance = ring_distance
        self.crystal_length = crystal_length

    def index_dims(self):
        return (self.nb_blocks, self.nb_detectors_per_ring // self.nb_blocks,
                self.nb_rings)

    def height(self):
        return self.nb_rings * self.ring_distance

    @property
    def nb_detectors_per_block(self):
        return self.nb_detectors_per_ring // self.nb_blocks * self.nb_rings
    
    @property
    def nb_detectors(self):
        return self.nb_detectors_per_ring * self.nb_rings

    @classmethod
    def from_json_file(cls, path):
        with open(path, 'r') as fin:
            return ScannerSpec(**json.load(fin))


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
            y, z = np.unravel_index(
                [self.crystal_id], spec.index_dims()[1:], order='F')
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
                np.ravel_multi_index(
                    [[self.y], [self.z]], spec.index_dims()[1:], order='F')[0],
                self.x)
        if cls == CrystalID3:
            return CrystalID3(self.x, self.y, self.z)
        raise TypeError("Can not convert to {}".format(cls))

    def __eq__(self, c):
        if isinstance(c, CrystalID3) and [self.x, self.y, self.z
                                          ] == [c.x, c.y, c.z]:
            return True
        return False

    def __repr__(self):
        return "<CrystalID3(x={}, y={}, z={})>".format(self.x, self.y, self.z)


class Crystal:
    def __init__(self, entity, id):
        self.entity = entity
        self.id = id


class CrystalFactory:
    def __init__(self, spec: ScannerSpec):
        self.spec = spec

    def create(self, crystal_id):
        crystal_size = self.spec.ring_distance
        id3 = crystal_id.to(CrystalID3, self.spec)
        z = id3.z * crystal_size - self.spec.height() / 2
        z = z + crystal_size / 2
        theta = 2 * np.pi / self.spec.nb_blocks * id3.x
        normal = [np.cos(theta), np.sin(theta), 0]
        center_of_block = np.array(
            [np.cos(theta), np.sin(theta)]) * (
                self.spec.inner_diameter / 2 + self.spec.crystal_length / 2)
        move = crystal_size * (
            id3.y - self.spec.nb_detectors_per_ring / self.spec.nb_blocks / 2 +
            0.5)
        x, y = center_of_block + np.array(
            [-move * np.sin(theta), move * np.cos(theta)])

        crystal_length = self.spec.ring_distance

        size = [crystal_length, crystal_length, self.spec.crystal_length]
        return Crystal(
            Box(size, [x, y, z], normal), id3.to(CrystalID2, self.spec))
