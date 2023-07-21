from gojos import model
from gojos.players import mens_players

def test_functional_version_of_player(configure_repo):
    model.Player.reset()
    pl = model.Player.new("R. McIlroy", klass_name="McIlroy")

    players = {'players': set()}

    player, players = model.player_for(configure_repo.players_graph(), players, klass_name="McIlroy")
    breakpoint()
    

def test_create_new_player(configure_repo):
    model.Player.reset()
    pl = model.Player.new("R. McIlroy", klass_name="McIlroy")

    assert pl.name == "R. McIlroy"

    assert pl == pl.__class__.cache_hit(name=pl.name).value
    assert pl == pl.__class__.cache_hit(klass_name=pl.klass_name).value

    same_pl = model.Player.load(name="R. McIlroy")

    assert same_pl == pl


def test_search_on(configure_repo_empty_players):
    model.Player.reset()
    add_players()

    pl1_name = model.Player.load(name="R. McIlroy")
    pl1_klass_name = model.Player.load(klass_name="McIlroy")

    assert pl1_name == pl1_klass_name


def test_load_all_players(configure_repo):
    model.Player.reset()
    add_players()

    model.Player.loadall()
    assert mens_players.McIlroy.name == "R. McIlroy"
    assert mens_players.Fleetwood.name == "T. Fleetwood"



def test_player_set_on_class_module(configure_repo):
    model.Player.reset()
    add_players()
    model.Player.loadall()

    assert mens_players.McIlroy.name == "R. McIlroy"
    assert mens_players.Fleetwood.name == "T. Fleetwood"


# def test_find_player_using_dot_and_sp(configure_repo_empty_players):
#     model.Player.clear_cache()
#     add_players()
#
#     pl = model.Player.load("C.Alcaraz")
#     pl_same = model.Player.load("Carlos Alcaraz")
#
#     assert pl.name == 'Carlos Alcaraz'
#     assert pl == pl_same


def test_find_player_not_defined(configure_repo_empty_players):
    add_players()

    assert not model.Player.load("Not A Real Name")


# def test_player_with_same_surname(configure_repo_empty_players):
#     model.Player.clear_cache()
#     add_players()
#     pl1 = model.Player.load("Francisco Cerundolo")
#
#     assert pl1.name == "Francisco Cerundolo"
#
#     alt_name_player = model.Player.load("F.Cerundolo")
#
#     assert alt_name_model.name == "Francisco Cerundolo"


def add_players():
    model.Player.new("R. McIlroy",
                      klass_name="McIlroy")
    model.Player.new("T. Fleetwood",
                      klass_name="Fleetwood")
    model.Player.new("S. Scheffler",
                      klass_name="Scheffler")