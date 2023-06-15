
from gojos.majors import tournaments
from gojos.model import tournament_event, tournament
from gojos.fantasy import points_strategy

from . import entries, results

LACC = tournament.Course(name="LA Country Club", country_symbol="USA", par=70)

USOpen2023 = (tournament_event.TournamentEvent(event_of=tournaments.USOpen, year=2023)
              .add_entries(entries.entries())
              .at_course(LACC)
              .fantasy_points_strategy(points_strategy.strategy_inverted_position_1_wc_4_max_players_10()))


tournaments.add_results(tournament=USOpen2023, results_module=results)
