import pytest
from gojos import model
from gojos.fantasy import points_strategy
from gojos.players import mens_players as players

from tests.fixtures import results


def create_tournie():
    return model.GrandSlam.create(name="Clojos Open", subject_name="ClojosOpen", perma_id="co")

def tournament_in_fantasy(tournament_to_return, _name):
    return tournament_to_return


# def clojos_open_2023_with_results():
#     tournie = clojos_open_2023()
#
#     tournaments.add_results(tournament=tournie, results_module=results)
#     return tournie


def clojos_open_2023():
    event = (model.TournamentEvent.create(tournament=create_tournie(), year=2023)
             .add_entries(entries())
             .fantasy_points_strategy(points_strategy.strategy_inverted_position_1_wc_2_max_players_4()))
    return event


@pytest.fixture
def build_players():
    model.Player.new(name="T. Fleetwood", klass_name="Fleetwood")
    model.Player.new(name="C. Morikawa", klass_name="Morikawa")
    model.Player.new(name="S. Scheffler", klass_name="Scheffler")
    model.Player.new(name="M. Fitzpatrick", klass_name="Fitzpatrick")
    model.Player.new(name="J. Rahm", klass_name="Rahm")
    model.Player.new(name="V. Hovland", klass_name="Hovland")
    model.Player.new(name="T. Hatton", klass_name="Hatton")
    model.Player.new(name="M. Homa", klass_name="Homa")
    model.Player.new(name="Z. Schauffele", klass_name="Schauffele")
    model.Player.new(name="R. McIlroy", klass_name="McIlroy")
    model.Player.new(name="T. Finau", klass_name="Finau")
    model.Player.loadall()

def entries():
    return [
        players.Fleetwood,
        players.Scheffler,
        players.Fitzpatrick,
        players.Rahm,
        players.Hovland,
        players.Hatton,
        players.Homa,
        players.Schauffele,
        players.McIlroy,
        players.Finau]
