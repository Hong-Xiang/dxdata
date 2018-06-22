import click


@click.command()
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
def generate(scanner, coincidence, hits, target):
    from ..generate import DatabaseGenerator, DataSpec
    generator = DatabaseGenerator(DataSpec(scanner, hits, coincidence, target))
    generator.generate()


if __name__ == "__main__":
    generate()