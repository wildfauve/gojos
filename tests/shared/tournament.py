from gojos.majors import tournaments
from gojos.model import tournament_event
from gojos import model
from gojos.fantasy import points_strategy
from gojos.players.mens_players import *

from tests.fixtures import results

ClojosOpen = model.GrandSlam(name="Clojos Open", subject_name="ClojosOpen", perma_id="co")


def tournament_in_fantasy(tournament_to_return, _name):
    return tournament_to_return


def clojos_open_2023_with_results():
    tournie = clojos_open_2023()

    tournaments.add_results(tournament=tournie, results_module=results)
    return tournie


def clojos_open_2023():
    tournie = (tournament_event.TournamentEvent(event_of=ClojosOpen, year=2023)
               .add_entries(entries())
               .fantasy_points_strategy(points_strategy.strategy_inverted_position_1_per_position_4_wildcards()))
    return tournie



def entries():
    return [
        Morikawa,
        Finau,
        Fleetwood,
        Scheffler,
        Fitzpatrick,
        Rahm,
        Hovland,
        Hatton,
        Homa,
        Schauffele,
        McIlroy,
        Rose,
        Day,
        Theegala,
        Burns,
        Spieth
    ]
