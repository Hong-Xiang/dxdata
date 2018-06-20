import pytest
from pathlib import Path


@pytest.fixture(scope='module')
def path_resource():
    return Path('/mnt/gluster/Resource')
