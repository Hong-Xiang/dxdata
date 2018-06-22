import pytest
from pathlib import Path
from dxl.data.zoo.incident_position_estimation.crystal import ScannerSpec
import json


@pytest.fixture(scope='module')
def path_resource():
    return Path('/mnt/gluster/Resource')


@pytest.fixture(scope='module')
def path_of_db():
    return '/mnt/gluster/CustomerTests/IncidentEstimation/SQLAlchemyDemo/simu0.1/gamma.db'


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
    with open(spec_of_block8_data['scanner_json'], 'r') as fin:
        return ScannerSpec(**json.load(fin))


