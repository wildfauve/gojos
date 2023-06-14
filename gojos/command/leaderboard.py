from typing import Dict
from functools import reduce, partial
from itertools import accumulate
from enum import Enum
from rich.console import Console
from rich.table import Table
from rich import box
import polars as pl

from gojos import dataframe, presenter
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
    scores = _format_team_scores(tournie, accum, teams_points_per_round(fantasy_teams, accum))

    return dataframe.build_df(scores)


def _show_df(df):
    presenter.event_team_scores_table(df)


def _show_old(fantasy_teams, round_number=None):
    table = Table(title=f"Leaderboard For Round {round_number if round_number else 'All'}", box=box.ROUNDED)

    table.add_column("Score", justify="center", style="cyan", no_wrap=True)
    table.add_column("Team", justify="left", style="magenta")

    rankings = sorted_teams(fantasy_teams, round_number)
    breakpoint()

    for team, score in rankings:
        table.add_row(f"{str(score)}", team.name)
    console.print(table)


def show_f1_leaderboard(fantasy_teams, round_number=None):
    results = total_f1_pts(fn.remove_none([f1_score_for_round(rd, fantasy_teams) for rd in range(1, total_rounds)]))

    table = Table(title=f"F1 Style Leaderboard For Round {round_number if round_number else 'All'}", box=box.ROUNDED)

    table.add_column("Score", justify="center", style="cyan", no_wrap=True)
    table.add_column("Team", justify="left", style="magenta")

    rankings = sorted_f1_teams(results)
    ljust_len = int(len(str(max([r[1] for r in rankings]))))
    for team, score in rankings:
        table.add_row(f"{str(score).ljust(ljust_len)}", team.name)
    console.print(table)


def f1_score_for_round(rd, fantasy_teams):
    sorted_scores_for_round = sorted_teams(fantasy_teams, rd)
    if all([sc[1] for sc in sorted_scores_for_round]):
        return [f1_by_team(team_f1_pos) for team_f1_pos in zip(sorted_scores_for_round, f1_points)]
    return None


def f1_by_team(f1_pos):
    return [f1_pos[0][0], f1_pos[1]]


def total_f1_pts(f1_scores):
    return reduce(aggregate_f1_team_score, [team for rd in f1_scores for team in rd], [])


def aggregate_f1_team_score(board, team_f1_score_for_rd):
    tm = find_team_on_board(team_f1_score_for_rd[0], board)
    if not tm:
        board.append(team_f1_score_for_rd)
        return board
    tm[1] += team_f1_score_for_rd[1]
    return board


def find_team_on_board(team, board):
    return fn.find(partial(_team_board_predicate, team), board)


def _team_board_predicate(team, team_on_board):
    return team == team_on_board[0]


def teams_points_per_round(fantasy_teams, accum):
    if not fantasy_teams:
        return []
    return [(team, _accumulate(team.points_per_round(), accum)) for team in fantasy_teams]


def _accumulate(scores, accum: bool):
    if not accum:
        return scores
    return list(accumulate(scores))

def sorted_teams(fantasy_teams, round_number):
    return sorted([(team, team.total_points(round_number)) for team in fantasy_teams], key=lambda t: t[1], reverse=True)


def sorted_f1_teams(fantasy_teams):
    return sorted([team for team in fantasy_teams], key=lambda t: t[1], reverse=True)


def _format_team_scores(tournie, accum: bool, scores):
    rd_scores = reduce(partial(_scores_dict, tournie, accum), _transpose_scores(scores), {})
    return {**{"teams": [team.name for team, _ in scores]}, **rd_scores}


def _scores_dict(tournie, accum: bool, acc, score_column):
    rd, scores = score_column
    schedule = tournie.fantasy_points_schedule(rd + 1, accum)
    pts_allocation = tournie.fantasy_points_allocation(rd + 1)
    return {**acc, **{f"Round-{rd + 1}\n({schedule[rd]})\n({pts_allocation})": list(scores)}}


def _transpose_scores(scores):
    return enumerate(list(zip(*[points for _, points in scores])))
