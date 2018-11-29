import click

from cli.cli import pass_context
from cli import __version__

@click.command()
@pass_context
def command(ctx, **kwargs):
    """Muestra versión y termina ejecución."""
    click.echo(f"Version: {__version__}")
    click.echo("")
    click.echo("config.yaml:")
    click.echo("-----------")
    click.echo("logger:")
    click.echo(" - verbose: {}".format(
             ctx.config['logger']['verbose']))
    click.echo("endpoint:")
    click.echo("  registro:")
    click.echo("    - dev: {}".format(
             ctx.config['endpoint']['registro']['dev']))
    click.echo("    - pre: {}".format(
             ctx.config['endpoint']['registro']['pre']))
    click.echo("    - prod: {}".format(
             ctx.config['endpoint']['registro']['prod']))
    click.echo("")
