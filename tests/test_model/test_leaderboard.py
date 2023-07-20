from gojos import model
from gojos import repo, fantasy
from gojos.players import mens_players

from tests.shared import *
from tests.fixtures import results


def setup_function():
    model.Tournament.reset()
    model.Round.reset()
    model.LeaderBoard.reset()
    model.TournamentEvent.reset()
    model.PlayerScore.reset()


def test_add_first_round_scores(configure_repo, build_players):
    event = clojos_open_2023()

    leaderboard = event.load().leaderboard

    assert not leaderboard.rounds

    results.round_1(event)

    leaderboard.for_round(1)

    assert leaderboard.positions_for_player_per_round(mens_players.Morikawa, []) == [1]
    assert leaderboard.positions_for_player_per_round(mens_players.Schauffele, []) == [10]


def test_add_2nd_round_scores(configure_repo, build_players):
    event = clojos_open_2023()

    leaderboard = event.load().leaderboard

    results.round_1(event)
    results.round_2(event)

    leaderboard.for_round(2)

    assert leaderboard.positions_for_player_per_round(mens_players.Fleetwood, []) == [3, 1]
    assert leaderboard.positions_for_player_per_round(mens_players.Finau, []) == [2, 9]
    assert leaderboard.positions_for_player_per_round(mens_players.Hatton, []) == [8, 9]


def test_missed_cut(configure_repo, build_players):
    event = clojos_open_2023()

    leaderboard = event.load().leaderboard

    results.round_1(event)
    results.round_2_with_mc(event)

    round2 = leaderboard.for_round(2)

    fleetwood = round2.scores_for_player(mens_players.Fleetwood)

    assert fleetwood.state == model.PlayerState.CUT
    assert fleetwood.rounds[round2.subject].get('state') == model.PlayerState.CUT


def test_load_the_event(configure_repo, build_players):
    event = clojos_open_2023_with_results()

    finder = model.tournament.tournaments()

    co2023 = finder.slam("ClojosOpen").for_year(2023, True)

    leaderboard = co2023.leaderboard

    assert leaderboard.positions_for_player_per_round(mens_players.Fleetwood, []) == [3, 1]
    assert leaderboard.positions_for_player_per_round(mens_players.Finau, []) == [2, 9]
    assert leaderboard.positions_for_player_per_round(mens_players.Hatton, []) == [8, 9]

# Helpers
