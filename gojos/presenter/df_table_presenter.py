from typing import List, Tuple
from pathlib import Path
from rich.table import Table
import polars as pl

from gojos.adapter import discord

from . import console


temp_file_path = Path("_temp") / "leaderboard.txt"

def event_team_scores_table(df: pl.DataFrame, to_discord: bool = False):
    general_df_table(df, Table(title="Fantasy Scores"), to_discord)
    ...

def leaderboard(df: pl.DataFrame, to_discord: bool = False):
    general_df_table(df, Table(title="Leaderboard"), to_discord)
    ...


def general_df_table(df, table, to_discord: bool = False):
    for column in df.columns:
        table.add_column(column, justify="right", style="green")

    for row in df.rows():
        table.add_row(*[str(item) for item in row])

    console.terminal_console().print(table)

    if to_discord:
        _send_to_discord(table)



def _send_to_discord(table):
    cons = console.to_string_console()
    cons.print(table)
    _as_text(cons)
    pass

def _as_text(cons):
    discord.send_basic_text(_format(cons.file.getvalue()))
    pass


def _as_attachment(cons):
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