from gojos.model import player
from gojos.players import mens_players


def test_create_new_player(configure_repo_empty_players):
    player.Player.clear_cache()
    pl = player.Player.new("R. McIlroy", klass_name="McIlroy")

    assert pl.name == "R. McIlroy"

    assert pl == pl.__class__.cache_hit(name=pl.name).value
    assert pl == pl.__class__.cache_hit(klass_name=pl.klass_name).value

    same_pl = player.Player.load(name="R. McIlroy")

    assert same_pl == pl


def test_search_on(configure_repo_empty_players):
    player.Player.clear_cache()
    add_players()

    pl1_name = player.Player.load(name="R. McIlroy")
    pl1_klass_name = player.Player.load(klass_name="McIlroy")

    assert pl1_name == pl1_klass_name


def test_load_all_players(configure_repo_empty_players):
    player.Player.clear_cache()
    add_players()

    player.Player.loadall()
    assert mens_players.McIlroy.name == "R. McIlroy"
    assert mens_players.Fleetwood.name == "T. Fleetwood"



def test_player_set_on_class_module(configure_repo_empty_players):
    player.Player.clear_cache()
    add_players()
    player.Player.loadall()

    assert mens_players.McIlroy.name == "R. McIlroy"
    assert mens_players.Fleetwood.name == "T. Fleetwood"


# def test_find_player_using_dot_and_sp(configure_repo_empty_players):
#     player.Player.clear_cache()
#     add_players()
#
#     pl = player.Player.load("C.Alcaraz")
#     pl_same = player.Player.load("Carlos Alcaraz")
#
#     assert pl.name == 'Carlos Alcaraz'
#     assert pl == pl_same


def test_find_player_not_defined(configure_repo_empty_players):
    player.Player.clear_cache()
    add_players()

    assert not player.Player.load("Not A Real Name")


# def test_player_with_same_surname(configure_repo_empty_players):
#     player.Player.clear_cache()
#     add_players()
#     pl1 = player.Player.load("Francisco Cerundolo")
#
#     assert pl1.name == "Francisco Cerundolo"
#
#     alt_name_player = player.Player.load("F.Cerundolo")
#
#     assert alt_name_player.name == "Francisco Cerundolo"


def add_players():
    player.Player.new("R. McIlroy",
                      klass_name="McIlroy")
    player.Player.new("T. Fleetwood",
                      klass_name="Fleetwood")
    player.Player.new("S. Scheffler",
                      klass_name="Scheffler")