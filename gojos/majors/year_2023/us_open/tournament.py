
from gojos.majors import tournaments
from gojos.model import tournament_event
from gojos.fantasy import points_strategy

from . import entries, results

USOpen2023 = (tournament_event.TournamentEvent(event_of=tournaments.USOpen, year=2023)
              .add_entries(entries.entries())
              .fantasy_points_strategy(points_strategy.strategy_inverted_position_1_per_position_4_wildcards()))


tournaments.add_results(tournament=USOpen2023, results_module=results)
