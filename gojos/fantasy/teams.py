from __future__ import annotations
from typing import Union
from functools import partial, reduce
import json

from rich.console import Console
from rich.table import Table
from rich import box

from gojos import model
from gojos.util import fn, echo

console = Console()

# TeamGelatoGiants = model.Team("Team Gelato Giants", "Bronzie & Juki")
# TeamPolarPrecision = model.Team("Team Polar Precision", "IceT, Pepsi, Rollie, Lemmie & Gertie")
# TeamHeroHangouts = model.Team("Team Hero Hangouts", "Marmalade, Richmond, Greenwich")
# TeamBearNecessities = model.Team("Team Bear Necessities", "Fraser, Tom, Frank, Spencer & Duck")
# TeamMusicalBears = model.Team("Team Musical Bears", "Rinksy, Beetie, Motzie")
# TeamFauve = model.Team("Team Fauve", "Perky")
# TeamClojo = model.Team("Team Clojo", "Claudie, Fyodoro")
# TeamLightHouse = model.Team("Team LightHouse", "Edouard, Piri")
#
# teams = [TeamGelatoGiants,
#          TeamPolarPrecision,
#          TeamHeroHangouts,
#          TeamBearNecessities,
#          TeamMusicalBears,
#          TeamClojo,
#          TeamLightHouse,
#          TeamFauve]
#

def build_graph(g):
    [team.build_graph(g) for team in teams]


def symbolised_names():
    return [t.symbolic_name for t in teams]


def points_details_all_teams(teams):
    return reduce(_team_points_aggregate, teams, {})


def _team_points_aggregate(accum, team):
    for_team = explain_points_for_team(team)
    return {**accum, **{team: for_team}}


def explain_points_for_team(team: Union[str, model.Team], teams=None):
    tm = find_team_by_name(team, teams) if isinstance(team, str) else team
    if not tm:
        echo.echo("Team Not Found")
        return None
    return tm.explain_points()



def find_team_by_name(team_name, teams):
    return fn.find(partial(_team_name_predicate, team_name), teams)


def find_team(team, teams):
    return fn.find(partial(_team_predicate, team), teams)


def _team_name_predicate(team_name, team):
    return team_name == team.symbolic_name


def _team_predicate(team_to_find, team):
    return team_to_find == team
