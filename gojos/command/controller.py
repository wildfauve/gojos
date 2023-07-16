from typing import Callable, Dict
import polars as pl

from . import leaderboard, fantasy_commands
from gojos import fantasy
from gojos.fantasy import teams, selections
from gojos.majors import tournaments
from gojos.util.data_scrapping import leaderboard_parser
from gojos.util import echo


def leaderboard_df(tournament_name,
                   tournament_search_fn: Callable = tournaments.tournament_in_fantasy,
                   fantasy_tournaments: Dict = fantasy.fantasy_tournaments) -> pl.DataFrame:
    tournie = _find_tournament_by_name(tournament_name, tournament_search_fn)
    if not tournie:
        return
    return leaderboard.current_leaderboard(tournie, _apply_fantasy(_start(tournie), fantasy_tournaments))


def rank_plot(file: str,
              tournament_name: str,
              ranking_plot: bool,
              tournament_search_fn: Callable = tournaments.tournament_in_fantasy,
              fantasy_tournaments: Dict = fantasy.fantasy_tournaments):
    tournie = _find_tournament_by_name(tournament_name, tournament_search_fn)
    if not tournie:
        return
    leaderboard.scores_plot(file, tournie, _apply_fantasy(_start(tournie), fantasy_tournaments), ranking_plot)
    pass


def cut_danger(tournament_name,
               tournament_search_fn: Callable = tournaments.tournament_in_fantasy,
               fantasy_tournaments: Dict = fantasy.fantasy_tournaments) -> pl.DataFrame:
    tournie = _find_tournament_by_name(tournament_name, tournament_search_fn)
    if not tournie:
        return
    return fantasy_commands.cut_danger(_apply_fantasy(_start(tournie), fantasy_tournaments))


def leaderboard_scrap(entries_file, players_file, leaderboard_file, for_round):
    leaderboard_parser.build_leaderboard(entries_file=entries_file,
                                         players_file=players_file,
                                         leaderboard_file=leaderboard_file,
                                         for_round=for_round)


def _find_tournament_by_name(for_name: str, tournament_search_fn: Callable):
    """
    imports tournament modules only when being used on the CLI.
    """
    tournie = tournament_search_fn(for_name)
    if not tournie:
        echo.echo(f"{for_name} does not exist as a tournament")
    return tournie


def _start(tournie):
    return tournie


def _apply_fantasy(tournie, fantasy_tournaments: Dict):
    fantasy_module = fantasy_tournaments.get(tournie.name, None)

    if not fantasy_module:
        echo.echo(f"No fantasy selections for {tournie.name}")
        return
    return selections.apply(fantasy_module, tournie)
