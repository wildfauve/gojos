from functools import reduce, partial

import polars as pl

from gojos.model import PlayerScore

from . import expr


def player_scores_to_leaderboard_df(player_scores: list[PlayerScore], for_round) -> pl.DataFrame:
    rd_cols = reduce(_rd, range(for_round), {})
    score_series = reduce(partial(_player_round_series, for_round), player_scores, _series(for_round, rd_cols))
    return expr.add_rd_total(pl.from_dict(score_series).sort('Pos'), rd_cols.keys())


def _series(for_round, rd_cols):
    return {
        **{'Player': [], 'Pos': []},
        **rd_cols
    }


def _rd(acc, rd):
    acc[f"Rd{rd + 1}"] = []
    return acc


def _player_round_series(for_round, acc, player_score):
    rd_scores = list(player_score.rounds_scores())
    acc['Player'].append(player_score.player.name)
    acc['Pos'].append(rd_scores[for_round - 1].get('current_pos'))
    for rd in range(for_round):
        acc[f"Rd{rd + 1}"].append(rd_scores[rd].get('score'))
    return acc
