from gojos import model

from tests.shared import tournament

def setup_function():
    model.Team.init()

def test_create_fantasy_tournament(configure_repo):
    team = create_team()

    event = tournament.clojos_open_2023()

    fantasy_major = team.major(event)

    breakpoint()



def create_team():
    return model.Team.create("Fauve", "Perky, Jacque, Albert", features=[])

