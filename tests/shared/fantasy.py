import pytest


from gojos import model

@pytest.fixture
def test_teams():
    return (model.Team.create("Bear Necessities", "a, b, c"),
            model.Team.create("Clojos", "d, e, f"),
            model.Team.create("Fauve", "d, e, f"))
