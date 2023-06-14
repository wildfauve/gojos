import polars as pl

from . import leaderboard
from gojos import fantasy
from gojos.fantasy import teams, selections
from gojos.majors import tournaments
from gojos.util.data_scrapping import leaderboard_parser


def leaderboard_df(tournament_name) -> pl.DataFrame:
    tournie = _find_tournament_by_name(tournament_name)
    if not tournie:
        return
    return leaderboard.current_leaderboard(tournie, _apply_fantasy(_start(tournie)))


def leaderboard_scrap(entries_file, players_file):
    leaderboard_parser.build_leaderboard(entries_file=entries_file,
                                         players_file=players_file)



def _find_tournament_by_name(for_name: str):
    """
    imports tournament modules only when being used on the CLI.
    """
    tournie = tournaments.tournament_in_fantasy(for_name)
    if not tournie:
        echo.echo(f"{for_name} does not exist as a tournament")
    return tournie


def _start(tournie):
    return tournie


def _apply_fantasy(tournie):
    fantasy_module = fantasy.fantasy_tournaments.get(tournie.name, None)

    if not fantasy_module:
        echo.echo(f"No fantasy selections for {tournie.name}")
        return

    return selections.apply(fantasy_module, tournie)
