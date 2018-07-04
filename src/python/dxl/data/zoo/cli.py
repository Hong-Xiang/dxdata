import click


class CLI(click.MultiCommand):
    commands = {'incident': None}

    def __init__(self):
        super(__class__, self).__init__(
            name='zoo',
            help='Data processing cli zoo (project specified tools).')

    def list_commands(self, ctx):
        return sorted(self.commands.keys())

    def get_command(self, ctx, name):
        from .incident.cli import incident
        if name in self.commands:
            if self.commands[name] is None:
                mapping = {'incident': incident}
                self.commands[name] = mapping.get(name)
        return self.commands.get(name)


zoo = CLI()