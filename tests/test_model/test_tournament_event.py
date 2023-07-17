from gojos import model
from gojos import repo, fantasy
from gojos.players import mens_players

from tests.shared import tournament


def test_create_event(configure_repo):
    tournament.create_tournie()

    event = model.TournamentEvent.create(year=2023, tournament_name="Clojos Open")

    assert event.scheduled_in_year == 2023
    assert event.is_event_of.name == "Clojos Open"

    same_event = model.TournamentEvent.get(tournament=event.is_event_of, year=2023)

    assert same_event == event


def test_make_event_from_tournament(configure_repo):
    tournie = tournament.create_tournie()

    event = tournie.make_event(year=2023)

    assert event.scheduled_in_year == 2023
    assert event.is_event_of.name == "Clojos Open"

    exactly_the_same_event = tournie.make_event(year=2023)
    assert id(event) == id(exactly_the_same_event)


def test_strategies(configure_repo):
    tournie = tournament.create_tournie()

    event = tournie.make_event(year=2023, cut_strategy=model.Cut.build("CutTop60AndTies"))


    assert isinstance(event.cut_strategy, model.CutTop60AndTies)
    assert isinstance(event.points_strategy, fantasy.InvertedPosition)

    same_event = model.TournamentEvent.get(tournament=event.is_event_of, year=2023)
    assert isinstance(same_event.points_strategy, fantasy.InvertedPosition)
    assert isinstance(same_event.cut_strategy, model.CutTop60AndTies)


def test_add_player_entries(configure_repo):
    tournie = tournament.create_tournie()

    event = tournie.make_event(year=2023, cut_strategy=model.Cut.build("CutTop60AndTies"))

    event.add_entries(['McIlroy', "Fleetwood"])

    assert set(event.entries) == {mens_players.McIlroy, mens_players.Fleetwood}

    same_event = model.TournamentEvent.get(tournament=event.is_event_of, year=2023)
    assert set(same_event.entries) == {mens_players.McIlroy, mens_players.Fleetwood}



def test_get_all_events(configure_repo):
    tournament.clojos_open_2023()

    results = model.TournamentEvent.get_all()

    assert len(results) == 1

    expected = {'ClojosOpen2023'}
    assert {ev.name for ev in results} == expected

    expected_tournies = {'Clojos Open'}
    assert {ev.is_event_of.name for ev in results} == expected_tournies


# Helpers
