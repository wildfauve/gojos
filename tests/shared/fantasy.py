import pytest

from tests.fixtures import tournie_teams

@pytest.fixture
def fantasy_tournaments():
    return {
        "ClojosOpen2023": tournie_teams
    }