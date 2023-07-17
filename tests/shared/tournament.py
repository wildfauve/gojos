from gojos.majors import tournaments
from gojos.model import tournament_event
from gojos import model
from gojos.fantasy import points_strategy
from gojos.players import mens_players as players

from tests.fixtures import results


def create_tournie():
    return model.GrandSlam.create(name="Clojos Open", subject_name="ClojosOpen", perma_id="co")

def tournament_in_fantasy(tournament_to_return, _name):
    return tournament_to_return


def clojos_open_2023_with_results():
    tournie = clojos_open_2023()

    tournaments.add_results(tournament=tournie, results_module=results)
    return tournie


def clojos_open_2023():
    event = (tournament_event.TournamentEvent.create(tournament=create_tournie(), year=2023)
             .add_entries(entries())
             .fantasy_points_strategy(points_strategy.strategy_inverted_position_1_wc_2_max_players_4()))
    return event


def entries():
    return [
        players.Fleetwood,
        players.Scheffler,
        players.Fitzpatrick,
        players.Rahm,
        players.Hovland,
        players.Hatton,
        players.Homa,
        players.Schauffele,
        players.McIlroy]
