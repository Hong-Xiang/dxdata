from typing import NamedTuple, Optional
from pathlib import Path

__all__ = ['QuerySpec', 'FeatureSpec']


class QuerySpec:
    def __init__(self, path, limit=None, chunk=None, offset=0):
        self.path = path
        self.limit = limit
        self.chunk = chunk
        self.offset = offset


class FeatureSpec:
    def __init__(self, main_feature=None, is_crystal_center=True,
                 is_crystal_index=None, padding_size=None, shuffle=None):
        self.main_feature = main_feature
        self.is_crystal_center = is_crystal_center
        self.is_crystal_index = is_crystal_center
        self.padding_size=padding_size
        self.shuffle = shuffle

    @property
    def _fields(self):
        return ('main_feature', 'is_crystal_center', 'is_crystal_index',
                'padding_size', 'shuffle')
