import pytest
from jinja2 import Environment, FileSystemLoader

from gojos import model
from gojos.fantasy import points_strategy
from gojos.players import mens_players as players

from tests import fixtures

environment = Environment(loader=FileSystemLoader("tests/fixtures/templates/"))

def create_tournie():
    return model.GrandSlam.create(name="Clojos Open", subject_name="ClojosOpen", perma_id="co")


def tournament_in_fantasy(tournament_to_return, _name):
    return tournament_to_return


def clojos_open_2023_with_results():
    event = clojos_open_2023().load()
    fixtures.round_1(event)
    fixtures.round_2(event)
    return event


def clojos_open_2023_with_3_rds_and_missed_cut():
    event = clojos_open_2023().load()
    fixtures.round_1(event)
    fixtures.round_2_with_mc(event)
    fixtures.round_3(event)
    return event


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
    return [players.Fleetwood,
            players.Scheffler,
            players.Fitzpatrick,
            players.Rahm,
            players.Hovland,
            players.Hatton,
            players.Homa,
            players.Schauffele,
            players.Finau,
            players.Morikawa]


@pytest.fixture
def empty_leaderboard_html():
    leaderboard_template = environment.get_template("leaderboard.html")
    context = {
        "csvw_json": open('tests/fixtures/templates/csvw_empty_scores.json', 'r').read()
    }
    return leaderboard_template.render(context)

@pytest.fixture
def r1_leaderboard_html():
    leaderboard_template = environment.get_template("leaderboard.html")
    context = {
        "csvw_json": open('tests/fixtures/templates/csvw_r1_scores.json', 'r').read()
    }
    return leaderboard_template.render(context)
