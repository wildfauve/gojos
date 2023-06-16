from typing import Dict
from functools import reduce, partial
from itertools import accumulate
from rich.console import Console
import polars as pl

from gojos import dataframe, presenter, plot
from gojos.util import fn

console = Console()


def current_leaderboard(tournie,
                        fantasy_teams,
                        accum: bool = True) -> pl.DataFrame:
    return _team_scores_df(tournie, fantasy_teams, accum)


def scores_plot(file: str, tournie, fantasy_teams, ranking_plot: bool = False):
    df = _team_scores_df(tournie, fantasy_teams, True)

    if ranking_plot:
        return plot.rank_plot(file, tournie, df)
    return plot.total_score_plot(file, tournie, df)


def _team_scores_df(tournie, fantasy_teams, accum: bool):
    scores = _format_team_scores(tournie, accum, _teams_points_per_round(fantasy_teams, accum))

    return dataframe.build_df(scores)


def _show_df(df):
    presenter.event_team_scores_table(df)


def find_team_on_board(team, board):
    return fn.find(partial(_team_board_predicate, team), board)


def _team_board_predicate(team, team_on_board):
    return team == team_on_board[0]


def _teams_points_per_round(fantasy_teams, accum):
    if not fantasy_teams:
        return []
    return [(team, _accumulate(team.points_per_round(), accum)) for team in fantasy_teams]


def _accumulate(scores, accum: bool):
    if not accum:
        return scores
    return list(accumulate(scores))


def sorted_teams(fantasy_teams, round_number):
    return sorted([(team, team.total_points(round_number)) for team in fantasy_teams], key=lambda t: t[1], reverse=True)


def _format_team_scores(tournie, accum: bool, scores):
    rd_scores = reduce(partial(_scores_dict, tournie, accum), _transpose_scores(scores), {})
    return {**{"teams": [team.name for team, _ in scores]}, **rd_scores}


def _scores_dict(tournie, accum: bool, acc, score_column):
    rd, scores = score_column
    return {**acc, **{f"Round-{rd + 1}": list(scores)}}


def _transpose_scores(scores):
    return enumerate(list(zip(*[points for _, points in scores])))
