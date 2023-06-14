from typing import Any
import click

def echo(msg: Any, ctx: dict = None):
    if ctx:
        click.echo(f"{msg} {ctx}")
        return None
    click.echo(msg)
