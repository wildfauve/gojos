from functools import partial
from gojos import command
import polars as pl

from gojos.fantasy import teams
from gojos import model
from gojos.players import mens_players as players

from tests.shared import *


# def test_leaderboard_with_no_results(fantasy_tournaments):
#     result = command.leaderboard_df('ClojosOpen2023',
#                                     tournament_search_fn=partial(tournament_in_fantasy, clojos_open_2023()),
#                                     fantasy_tournaments=fantasy_tournaments)
#
#     assert isinstance(result, pl.DataFrame)
#     assert result.rows() == [('Team Clojo',), ('Team Bear Necessities',)]
#
#
# def test_leaderboard_with_r2_results_accumulated(fantasy_tournaments):
#     tournie = clojos_open_2023_with_results()
#     result = command.leaderboard_df('ClojosOpen2023',
#                                     tournament_search_fn=partial(tournament_in_fantasy, tournie),
#                                     fantasy_tournaments=fantasy_tournaments)
#
#     df = result.filter(pl.col('teams') == "Team Clojo")
#
#     team, *points = df.rows()[0]
#
#     expected_pos = [[6, 7, 10, 8], [6, 7, 10, 8]]
#     expected_pts = [10 - pos + 1 for round_pos in expected_pos for pos in round_pos]
#
#     assert points[-1] == sum(expected_pts)
#
#
# def test_wildcard(fantasy_tournaments):
#     tournie = clojos_open_2023_with_results()
#     result = command.leaderboard_df('ClojosOpen2023',
#                                     tournament_search_fn=partial(tournament_in_fantasy, tournie),
#                                     fantasy_tournaments=fantasy_tournaments)
#
#     df = result.filter(pl.col('teams') == "Team Clojo")
#
#     assert df.rows()[0][2] == 26
#
#     teams.TeamClojo.major(tournie).play_wildcard(
#         model.WildCard().from_round(1).trade_out(players.Schauffele).trade_in(players.Morikawa))
#
#     result_after_wc = command.leaderboard_df('ClojosOpen2023',
#                                              tournament_search_fn=partial(tournament_in_fantasy, tournie),
#                                              fantasy_tournaments=fantasy_tournaments)
#     df_after_wc = result_after_wc.filter(pl.col('teams') == "Team Clojo")
#
#     assert df_after_wc.rows()[0][2] == 26 + 18
