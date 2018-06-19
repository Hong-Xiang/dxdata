import click


class CLI(click.MultiCommand):
    commands = {
        'image': None
    }

    def __init__(self):
        super(__class__, self).__init__(name='statistics', help='Statistic utilities')

    def list_commands(self, ctx):
        return sorted(self.commands.keys())

    def get_command(self, ctx, name):
        from ..image.cli import cli as image_cli
        if name in self.commands:
            if self.commands[name] is None:
                mapping = {'image': image_cli}
                self.commands[name] = mapping.get(name)
        return self.commands.get(name)


cli = CLI()


