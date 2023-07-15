from gojos.majors import tournaments
from gojos.model import tournament_event, tournament
from gojos.fantasy import points_strategy

from . import entries, leaderboard

RoyalLiverpool = tournament.Course(name="Royal Liverpool", country_symbol="SCO", par=70)

TheOpen2023 = (tournament_event.TournamentEvent(event_of=tournaments.TheOpen, year=2023)
               .add_entries(entries.entries())
               .at_course(RoyalLiverpool)
               .has_cut_strategy(tournament.CutTop60AndTies())
               .fantasy_points_strategy(points_strategy.strategy_inverted_position_1_wc_4_max_players_10()))

tournaments.add_results(tournament=TheOpen2023, results_module=leaderboard)
