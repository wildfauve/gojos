import pytest
from pathlib import Path

from gojos import repo, model

PLAYERS_PATH = (Path(__file__).parent.parent / "fixtures" / "test_players.ttl")
FANTASY_PATH = (Path(__file__).parent.parent / "fixtures" / "test_fantasy.ttl")
EMPTY_PLAYERS_PATH = (Path(__file__).parent.parent / "fixtures" / "test_empty_players.ttl")


@pytest.fixture
def configure_repo():
    repo.RepoContext().configure(players_triples_location=PLAYERS_PATH,
                                 fantasy_triples_location=FANTASY_PATH)
    repo.init()
    yield repo
    repo.drop()

@pytest.fixture
def configure_repo_empty_players():
    repo.RepoContext().configure(players_triples_location=EMPTY_PLAYERS_PATH,
                                 fantasy_triples_location=FANTASY_PATH)
    repo.init()
    yield repo
    repo.drop()


@pytest.fixture
def empty_graph():
    return repo.triples.graph()

