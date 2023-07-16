from gojos import model

def setup_function():
    model.Team.init()

def test_create_fantasy_team(configure_repo):
    team = model.Team.create("Fauve", "Perky, Jacque, Albert",
                             features=[])

    assert team.name == "Fauve"

    same_team = model.Team.get("Fauve")

    assert team == same_team


def test_get_all(configure_repo):
    create()
    teams = model.Team.get_all()

    assert {t.name for t in teams} == {"t1", "t2"}



def create():
    model.Team.create("t1", "a, b, c")
    model.Team.create("t2", "d, e, f")

