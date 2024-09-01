# -*- coding: utf-8 -*-

import click

from api_key_factory.factory.key import Key


@click.group()
@click.version_option("1.0.0", prog_name="api_key_factory")
def cli() -> None:
    """A simple CLI tool to generate API keys and their corresponding
    SHA-256 hashes.
    """
    pass


@cli.command()
@click.option(
    "-n",
    "--num",
    "num",
    type=click.IntRange(min=1),
    default=1,
    help="Number of API keys to generate",
)
def generate(
    num: int,
) -> None:
    """Command to generate API keys and their corresponding SHA-256 hashes.

    Args:
        num (int): Number of API keys to generate. Default 1.

    Raises:
        click.ClickException: Error when writing output file
    """
    for _ in range(num):
        key = Key()
        click.echo(f"{key.get_value()}   {key.get_hash()}")


if __name__ == "__main__":
    cli()  # pragma: no cover
