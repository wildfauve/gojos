from functools import partial
from gojos import command
import polars as pl

from tests.shared import *


def test_leaderboard_with_no_results(fantasy_tournaments):
    result = command.leaderboard_df('ClojosOpen2023',
                                    tournament_search_fn=partial(tournament_in_fantasy, clojos_open_2023()),
                                    fantasy_tournaments=fantasy_tournaments)

    assert isinstance(result, pl.DataFrame)
    assert result.rows() == [('Team Clojo',), ('Team Bear Necessities',)]


def test_leaderboard_with_r1_results(fantasy_tournaments):
    tournie = clojos_open_2023_with_results()
    result = command.leaderboard_df('ClojosOpen2023',
                                    tournament_search_fn=partial(tournament_in_fantasy, tournie),
                                    fantasy_tournaments=fantasy_tournaments)

    df = result.filter(pl.col('teams') == "Team Clojo")

    team, score = df.rows()[0]

    expected_pos = [11, 4, 12, 6, 7, 13, 10, 14, 15, 16]
    expected_pts = [16 - pos + 1 for pos in expected_pos]

    assert score == sum(expected_pts)
