import click
import json

from dxl.core.debug import enter_debug


@click.group()
def make():
    enter_debug()


@make.command()
@click.option(
    '--scanner',
    '-s',
    type=click.types.Path(exists=True, file_okay=True, dir_okay=False))
@click.option(
    '--coincidence',
    '-c',
    type=click.types.Path(exists=True, file_okay=True, dir_okay=False))
@click.option(
    '--hits',
    '-h',
    type=click.types.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('--target', '-t', type=click.types.Path(exists=False))
def db(scanner, coincidence, hits, target):
    """
    Generate database from csv files.
    """
    from ..generate import DatabaseGenerator, DataSpec
    generator = DatabaseGenerator(DataSpec(scanner, hits, coincidence, target))
    generator.generate()


@make.command()
@click.option(
    '--path_db',
    '-d',
    type=click.types.Path(exists=True, file_okay=True, dir_okay=False))
@click.option(
    '--path_table',
    '-t',
    type=click.types.Path(exists=False, file_okay=True, dir_okay=False))
@click.option('--padding-size', '-s', type=int, default=5,
              help='Padding size for hits of one photon. Photon with more hits than padding-size would be dropped.')
@click.option('--true-position', is_flag=True, help='Use true xyz of hit instead of center of crystal')
def table(path_db, path_table, true_position, padding_size):
    from ..table import make_table
    from ..function import sort_hits_by_energy
    make_table(path_db, path_table, not true_position,
               padding_size, sort_hits_by_energy)


@make.command()
def test():
    from dxl.data.zoo.incident_position_estimation.data import PhotonColumns, CoincidenceColumns
    from dxl.data.zoo.incident_position_estimation.function.on_columns import raw_columns2shuffled_hits_columns
    from dxl.data.zoo.incident_position_estimation.function import sort_hits_by_energy, coincidence2shuffled_hits
    from dxl.data.zoo.incident_position_estimation.database import nb
    path_db = '/mnt/gluster/hongxwing/Workspace/IncidentEstimation/data/gamma.db'
    limit, chunk = 1000, 1000
    cc = CoincidenceColumns(path_db, True, limit, chunk)
    shuffled_columns = raw_columns2shuffled_hits_columns(
        cc, 5, sort_hits_by_energy)
