from typing import List
from functools import reduce, partial

import polars as pl

from gojos import model, fantasy
from gojos.util import echo
from . import leaderboard


def build_leaderboard(tournament: model.Tournament,
                      year: int,
                      to_discord,
                      fantasy_tournaments_dict=fantasy.fantasy_tournaments) -> pl.DataFrame:
    event = tournament.for_year(year, load=True)
    if not event:
        return
    return leaderboard.current_leaderboard(event, _apply_fantasy(event, fantasy_tournaments_dict))


def rank_plot(file: str,
              tournament: model.Tournament,
              year: int,
              ranking_plot: bool,
              fantasy_tournaments_dict=fantasy.fantasy_tournaments):
    event = tournament.for_year(year, load=True)
    if not event:
        return
    leaderboard.scores_plot(file, event, _apply_fantasy(event, fantasy_tournaments_dict), ranking_plot)
    pass


def cut_danger(tournament: model.Tournament,
               year: int,
               for_round: int,
               to_discord,
               fantasy_tournaments_dict=fantasy.fantasy_tournaments) -> pl.DataFrame:
    event = tournament.for_year(year, load=True)
    if not event:
        return
    return _assess_cut_danger(_apply_fantasy(event, fantasy_tournaments_dict), for_round)


def _assess_cut_danger(fantasy_teams, for_round):
    return reduce(partial(_cut_danger_for_team, for_round), fantasy_teams, {})


def _cut_danger_for_team(for_round, accum, team):
    return {**accum, **{team: team.players_relative_to_cut(for_round)}}


def _apply_fantasy(event, fantasy_tournaments_dict) -> List[model.Team]:
    fantasy_module = fantasy_tournaments_dict.get(event.name, None)

    if not fantasy_module:
        echo.echo(f"No fantasy selections for {event.name}")
        return
    return fantasy.apply_selections(fantasy_module, event)
