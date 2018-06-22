import click


@click.command()
@click.option(
    '--coincidence',
    '-c',
    type=click.types.Path(exists=True, file_okay=True, dir_okay=False))
@click.option(
    '--hits',
    '-h',
    type=click.types.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('--target', '-t', type=click.types.Path(exists=False))
def generate(coincidence, hits, target):
    from ..generate import main
    main(coincidence_csv=coincidence, hits_csv=hits, target=target)


if __name__ == "__main__":
    generate()