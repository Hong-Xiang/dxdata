from typing import NamedTuple, Optional
from pathlib import Path

__all__ = ['QuerySpec', 'FeatureSpec']


class QuerySpec(NamedTuple):
    path: Path
    limit: Optional(int)
    chunk: Optional(int)
    offset: Optional(int)


class FeatureSpec(NamedTuple):
    main_feature: str
    is_crystal_center: bool
    is_crystal_index: bool
    is_padding: bool
    shuffle: str
