from gojos import model
from gojos import repo

def setup_function():
    model.Tournament.reset()
    model.TournamentEvent.reset()


def test_create_tournament(configure_repo):
    tournie = model.GrandSlam.create(name="The Open", subject_name="TheOpen", perma_id="to")

    assert tournie.name == "The Open"

    same_tournie = model.GrandSlam.get(name="The Open")

    assert same_tournie == tournie


def test_get_all_tournies(configure_repo):
    create_tournies()

    results = model.GrandSlam.get_all()

    assert len(results) == 4
    expected = {'Masters', 'US PGA', 'The Open', 'US Open'}
    assert {t.name for t in results} == expected

def test_get_all_with_events(configure_repo):
    create_tournies()
    create_events()
    finder = model.tournament.tournaments()

    to = finder.slam("TheOpen")
    assert to.name == "The Open"

    to, to2023 = finder.slam_year("TheOpen", 2023)
    assert to.name == "The Open"
    assert to2023.name == "TheOpen2023"




# Helpers

def create_tournies():
    model.GrandSlam.create(name="Masters", subject_name="Masters", perma_id="ms")
    model.GrandSlam.create(name="US PGA", subject_name="USPga", perma_id="up")
    model.GrandSlam.create(name="US Open", subject_name="USOpen", perma_id="us")
    model.GrandSlam.create(name="The Open", subject_name="TheOpen", perma_id="to")


def create_events():
    model.TournamentEvent.create(year=2023, tournament_name="Masters")
    model.TournamentEvent.create(year=2023, tournament_name="US Open")
    model.TournamentEvent.create(year=2023, tournament_name="US PGA")
    model.TournamentEvent.create(year=2023, tournament_name="The Open")
