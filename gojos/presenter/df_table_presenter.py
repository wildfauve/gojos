from typing import List, Tuple
from pathlib import Path
from rich.table import Table
import polars as pl

from gojos.adapter import discord

from . import console


temp_file_path = Path("_temp") / "leaderboard.txt"

def event_team_scores_table(df: pl.DataFrame, to_discord: bool = False):
    table = Table(title="Fantasy Scores")

    for column in df.columns:
        table.add_column(column, justify="right", style="green")

    for row in df.rows():
        table.add_row(*[str(item) for item in row])

    console.terminal_console().print(table)

    if to_discord:
        _send_to_discord_as_attachment(table)


def _send_to_discord(table):
    cons = console.to_string_console()
    cons.print(table)
    discord.send_basic_text(_format(cons.file.getvalue()))
    pass

def _send_to_discord_as_attachment(table):
    cons = console.to_string_console()
    cons.print(table)
    with open(temp_file_path, 'w') as f:
        f.write(cons.file.getvalue())
    discord.send_attachment(msg_title=f"Fantasy Leaderboard",
                            description="",
                            file_path=temp_file_path,
                            file_name=f"leaderboard.md",
                            as_attachment=False)
    temp_file_path.unlink(missing_ok=False)
    pass


def _format(table_str) -> str:
    return f"""
```
{table_str}
```
"""