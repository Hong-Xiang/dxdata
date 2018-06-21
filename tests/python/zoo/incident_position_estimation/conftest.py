import pytest
from pathlib import Path


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
