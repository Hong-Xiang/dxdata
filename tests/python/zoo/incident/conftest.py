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
def spec_of_block8_data():
    root = Path(
        '/mnt/gluster/CustomerTests/IncidentEstimation/SQLAlchemyDemo/simu0.1')
    return {
        'scanner_json': root / 'scanner.json',
        'hits_csv': root / 'hitsM.csv',
        'coincidences_csv': root / 'true_scatter_randomM.csv'
    }


@pytest.fixture(scope='module')
def scanner_spec(spec_of_block8_data):
    from dxl.data.zoo.incident.database.crystal import ScannerSpec
    with open(spec_of_block8_data['scanner_json'], 'r') as fin:
        return ScannerSpec(**json.load(fin))