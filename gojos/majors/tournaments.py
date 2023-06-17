from typing import List
import importlib
import re

from gojos import model
from gojos.util import monad

USOpen = model.GrandSlam(name="US Open", subject_name="USOpen", perma_id="uo")

TournamentLoaderConfig = {
    'USOpen2023': (2023, "us_open"),
}


def tournament_names():
    return TournamentLoaderConfig.keys()


def tournament_in_fantasy(name):
    """
    Takes a tournament name and dynamically loads the tournament module associated with that tournament.
    For example, if the name is AustralianOpen2023, the module loaded is ao.majors.year_2023.australian_open.tournament


    :param name:
    :return:
    """
    if name not in tournament_names():
        return None
    year, tournament_module_name = TournamentLoaderConfig.get(name)
    tournament_module = importlib.import_module(f"gojos.majors.year_{year}.{tournament_module_name}.tournament")
    return getattr(tournament_module, name)


def add_results(tournament, results_module):
    results = _rounds_from_leaderboard(results_module, tournament)
    return results


def _rounds_from_leaderboard(leaderboard_module, tournament):
    [_apply_scores(tournament, leaderboard_module, rd) for rd in range(1, 5)]
    return tournament


def _apply_scores(tournament, leaderboard_module, rd):
    mod = _import_round(leaderboard_module, rd)
    if mod.is_left():
        return None
    getattr(mod.value, 'scores')(tournament)
    pass


@monad.monadic_try()
def _import_round(leaderboard_module, round_number):
    return importlib.import_module(f"{leaderboard_module.__name__}.round{round_number}")
