import io

from rich.console import Console
from rich import print
from rich.panel import Panel


def terminal_console():
    return Console()


def to_string_console():
    return Console(file=io.StringIO(), width=120)


def panel():
    return Panel


def console_print(obj):
    print(obj)
