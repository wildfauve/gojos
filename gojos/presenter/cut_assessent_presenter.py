from typing import List, Tuple, Dict
from pathlib import Path
from rich.table import Table
import polars as pl

from gojos.adapter import discord

from . import console

temp_file_path = Path("_temp") / "cut_assessment.txt"


def cut_assessment_table(assessment: Dict, to_discord: bool = False):
    table = Table(title="Cut Assessment For Teams")

    table.add_column('Team', justify="right", style="cyan")
    table.add_column('Player', justify="right", style="magenta")
    table.add_column('Current Position', justify="right", style="magenta")
    table.add_column('Cut Assessment', justify="right")

    for team, players_assessments in assessment.items():
        table.add_row('', '', '', '')
        for player, latest_pos, assessment in players_assessments:
            table.add_row(team.name,
                          player.name,
                          str(latest_pos),
                          _cut_assessment(assessment))

    console.terminal_console().print(table)

    if to_discord:
        _send_to_discord_as_attachment(table)


def _cut_assessment(relative_position):
    if relative_position == 0:
        return '[orange]On Cut Line'
    if relative_position > 0:
        return f"[green]Above Cut by {relative_position}"
    return f"[bold red]Below Cut by {abs(relative_position)}"


def _send_to_discord(table):
    cons = console.to_string_console()
    cons.print(table)
    discord.send_basic_text(_format(cons.file.getvalue()))
    pass


def _send_to_discord_as_attachment(table):
    cons = console.to_string_console()
    cons.print(table)
    _as_attachment(cons)
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
