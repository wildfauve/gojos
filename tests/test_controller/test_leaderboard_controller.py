from functools import partial
from gojos import command
import polars as pl

from gojos.fantasy import teams
from gojos import model
from gojos.players import mens_players as players

from tests.shared import *
from tests import fixtures


def setup_function():
    model.Team.reset()
    model.Tournament.reset()
    model.Round.reset()
    model.LeaderBoard.reset()
    model.TournamentEvent.reset()
    model.PlayerScore.reset()


def test_leaderboard_with_no_results(configure_repo, build_players, test_teams):
    finder, _, _ = create_event_no_results()

    df = command.build_leaderboard(tournament=finder.slam("ClojosOpen"),
                                   year=2023,
                                   to_discord=False,
                                   fantasy_tournaments_dict=fixtures.fantasy_tournaments)

    assert isinstance(df, pl.DataFrame)
    assert set(df.rows()) == {('Bear Necessities', 0), ('Clojos', 0), ('Fauve', 1)}


def test_leaderboard_with_r2_results_accumulated(configure_repo, build_players, test_teams):
    finder, _, leaderboard = create_event_with_results()

    df = command.build_leaderboard(tournament=finder.slam("ClojosOpen"),
                                   year=2023,
                                   to_discord=False,
                                   fantasy_tournaments_dict=fixtures.fantasy_tournaments)

    fleetwood = leaderboard.positions_for_player_per_round(players.Fleetwood, [])
    homa = leaderboard.positions_for_player_per_round(players.Homa, [])

    bn = df.filter(pl.col('Teams') == "Bear Necessities")

    team, *points = bn.rows()[0]

    expected_pts = [10 - pos.get('current_pos') + 1 for pos in fleetwood]

    assert points[1] == expected_pts[0]
    assert points[2] == sum(expected_pts)


def test_wildcard(configure_repo, build_players, test_teams):
    finder, _, leaderboard = create_event_with_results()

    df = command.build_leaderboard(tournament=finder.slam("ClojosOpen"),
                                   year=2023,
                                   to_discord=False,
                                   fantasy_tournaments_dict=fixtures.fantasy_tournaments)

    fu = df.filter(pl.col('Teams') == "Fauve")

    fleetwood = leaderboard.positions_for_player_per_round(players.Fleetwood, [])
    homa = leaderboard.positions_for_player_per_round(players.Homa, [])

    expected_pts = [10 - pos.get('current_pos') + 1 for pos in [fleetwood[0], homa[1]]]

    assert fu.rows()[0][3] == sum(expected_pts)

def test_leaderboard_with_r3_with_mc(configure_repo, build_players, test_teams):
    finder, _, leaderboard = create_event_with_r3_mc()

    df = command.build_leaderboard(tournament=finder.slam("ClojosOpen"),
                                   year=2023,
                                   to_discord=False,
                                   fantasy_tournaments_dict=fixtures.fantasy_tournaments)

    fleetwood = leaderboard.positions_for_player_per_round(players.Fleetwood, [])

    assert model.PlayerState.CUT in fleetwood

    expected_pts = [10 - pos.get('current_pos') + 1 for pos in fleetwood[:-1]] + [1]

    bn = df.filter(pl.col('Teams') == "Bear Necessities")

    assert bn.rows()[0][4] == sum(expected_pts)


# Helpers

def create_event_with_results():
    event = clojos_open_2023_with_results()
    finder = model.tournament.tournaments()
    return finder, event, event.leaderboard


def create_event_with_r3_mc():
    event = clojos_open_2023_with_3_rds_and_missed_cut()
    finder = model.tournament.tournaments()
    return finder, event, event.leaderboard


def create_event_no_results():
    event = clojos_open_2023()
    finder = model.tournament.tournaments()
    return finder, event, event.leaderboard
