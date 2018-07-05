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
@click.option('--nb-max-hits', type=int)
@click.option('--nb-max-coincidence', type=int)
def db(scanner, coincidence, hits, target, nb_max_hits, nb_max_coincidence):
    """
    Generate database from csv files.
    """
    from dxl.data.zoo.incident.database.generate import DatabaseGenerator, DataSpec
    generator = DatabaseGenerator(DataSpec(scanner, hits, coincidence, target), nb_max_hits, nb_max_coincidence)
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
@click.option('--limit', '-l', type=int, help='Number of samples to convert.')
@click.option('--chunk', '-c', type=int, help='Database load chunk size.')
@click.option('--coincidence', is_flag=True, help='Convert conincidence instead of photons')
def table(path_db, path_table, true_position, padding_size, limit, coincidence, chunk):
    """
    Generate HDF5(PyTables) from database
    """
    from ..io.make_table import make_table
    from ..function import sort_hits_by_energy
    added = make_table(path_db, path_table, not true_position,
                       coincidence, padding_size,
                       sort_hits_by_energy, limit, chunk)
    click.echo("Added {} samples.".format(added))
