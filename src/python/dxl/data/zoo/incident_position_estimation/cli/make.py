import click
import json


@click.group()
def make():
    pass


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
