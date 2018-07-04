import pytest
from pathlib import Path
import json


@pytest.fixture(scope='module')
def path_resource():
    return Path('/mnt/gluster/Resource/dxdata/zoo/incident')


@pytest.fixture(scope='module')
def path_of_db(path_resource):
    return path_resource / 'data' / 'gamma.db'

@pytest.fixture(scope='module')
def query_spec(path_of_db):
    from dxl.data.zoo.incident.data import QuerySpec
    return QuerySpec(path_of_db, None, 1000, 0)

@pytest.fixture(scope='module')
def spec_of_block8_data(path_resource):
    root = path_resource / 'data'
    return {
        'scanner_json': root / 'scanner.json',
        'hits_csv': root / 'hits.csv',
        'coincidences_csv': root / 'coincidence.csv'
    }


@pytest.fixture(scope='module')
def scanner_spec(spec_of_block8_data):
    from dxl.data.zoo.incident.database.crystal import ScannerSpec
    with open(spec_of_block8_data['scanner_json'], 'r') as fin:
        return ScannerSpec(**json.load(fin))
