from typing import List
import importlib
import re

from gojos import model

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
    results = _for_round(results_module, tournament)
    return results


def _for_round(results_module, tournament):
    return _for_rd_fn_caller(results_module, tournament)


def _for_rd_fn_caller(results_module, tournament):
    [getattr(results_module, f)(tournament) for f in dir(results_module) if re.match(f"^round_", f)]
    return tournament
