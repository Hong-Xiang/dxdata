import click


class CLI(click.MultiCommand):
    commands = {'statistics': None, 'db': None, 'zoo': None}

    def __init__(self):
        super().__init__(
            name='dxdata', help='Data processing CLI.')

    def list_commands(self, ctx):
        return sorted(self.commands.keys())

    def get_command(self, ctx, name):
        from ..database.cli import database
        from dxl.data.zoo.cli import zoo
        if name in self.commands:
            if self.commands[name] is None:
                mapping = {'db': database, 'zoo': zoo}
                self.commands[name] = mapping.get(name)
        return self.commands.get(name)


dxdata = CLI()
