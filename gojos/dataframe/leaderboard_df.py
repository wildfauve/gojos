from functools import reduce, partial

import polars as pl

from gojos.model import PlayerScore

from . import expr
from ..util import fn


def player_scores_to_leaderboard_df(player_scores: list[PlayerScore], for_round) -> pl.DataFrame:
    rd_cols = reduce(_rd, range(for_round), {})
    score_series = reduce(partial(_player_round_series, for_round), player_scores, _series(for_round, rd_cols))
    r = expr.add_rd_total(pl.from_dict(score_series), rd_cols.keys())

    return r.sort('Pos')


def _series(for_round, rd_cols):
    return {
        **{'Player': [], 'Pos': []},
        **rd_cols
    }


def _rd(acc, rd):
    acc[f"Rd{rd + 1}"] = []
    return acc


def _player_round_series(for_round, acc, player_score):
    # The rounds are in reverse order
    find_fn = partial(_find_rd_score, list(player_score.rounds_scores()))
    acc['Player'].append(player_score.player.name)
    rd_scr = find_fn(for_round)
    acc['Pos'].append(rd_scr.get('current_pos'))
    for rd in range(for_round):
        rd_score = find_fn(rd + 1)
        acc[f"Rd{rd + 1}"].append(rd_score.get('score'))
    return acc


def _find_rd_score(rd_scores, rd):
    return fn.find(lambda scr: scr.get('round_number') == rd, rd_scores)