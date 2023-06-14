from typing import Dict, Tuple
from functools import reduce
from collections import ChainMap
from pathlib import Path

from rich.table import Table

from gojos.adapter import discord
from . import console

accum_points = 0

temp_file_path = Path("_temp") / "explain.txt"

def explain(team_name, team_explain: Dict, to_discord: bool = False):
    table = Table(title=f"Points Explanation for {team_name}")

    table.add_column("Event", justify="center", style="green")
    table.add_column("Match", justify="center", style="green")
    table.add_column("Fantasy Selections", justify="center", style="green")
    table.add_column("Fantasy Scores", justify="left", style="green")
    table.add_column("Accumulated", justify="center", style="green")

    for ev in team_explain:
        for match in ev['matches']:
            table.add_row(ev['event'],
                          _match_summary(match),
                          _fantasy_selections(match),
                          _fantasy_scores(match),
                          str(accum_points))

    console.terminal_console().print(table)
    if to_discord:
        _send_to_discord(team_name, table)

    # echo.echo(json.dumps(team.explain_points(), indent=4))


def _send_to_discord(team_name, table):
    cons = console.to_string_console()
    cons.print(table)
    with open(temp_file_path, 'w') as f:
        f.write(cons.file.getvalue())
    discord.send_attachment(msg_title=f"Fantasy Score Explanation for {team_name}",
                            description="",
                            file_path=temp_file_path,
                            file_name=f"{team_name}-explain.txt",
                            as_attachment=False)
    temp_file_path.unlink(missing_ok=False)
    pass


def _format(table_str) -> str:
    return f"""
```
{table_str}
```
"""


def _match_summary(match):
    if not match['selected-winner']:
        return f"{match['match']}\n{match['between']}\n NOT COMPLETED\n"
    return f"{match['match']}\n{match['between']}\nWinner: {match['result-winner']} in {match['result-in-sets']} Sets"


def _fantasy_selections(match):
    if not match['selected-winner']:
        return "NO SELECTIONS"
    return f"""Selected: {match['selected-winner']} in {match['selected-in-sets']} Sets
"""


def _fantasy_scores(match):
    global accum_points
    total_pts, to_print = reduce(_points_reduce, dict(ChainMap(*match['points'])).items(), (0, ""))
    accum_points += total_pts
    return f"Total: {total_pts}\n{to_print}\n\n"


def _points_reduce(acc: Tuple[int, str], pt_item):
    pt_name, pts = pt_item
    total_pts, str_to_print = acc
    return total_pts + pts, str_to_print + f"{pt_name}: {pts}\n"
