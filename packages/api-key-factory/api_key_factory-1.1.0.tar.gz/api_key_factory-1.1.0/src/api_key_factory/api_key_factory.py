# -*- coding: utf-8 -*-

import click

from api_key_factory.factory.key import Key


@click.group()
@click.version_option("1.1.0", prog_name="api_key_factory")
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
@click.option(
    "-p",
    "--prefix",
    "prefix",
    type=str,
    default="",
    help="Add a prefix at the beginning of the key",
)
def generate(
    num: int,
    prefix: str,
) -> None:
    """Command to generate API keys and their corresponding SHA-256 hashes.

    Args:
        num (int): Number of API keys to generate. Default 1.

    Raises:
        click.ClickException: Error when writing output file
    """
    for _ in range(num):
        key = Key(prefix)
        click.echo(f"{key.get_value()}   {key.get_hash()}")


if __name__ == "__main__":
    cli()  # pragma: no cover
