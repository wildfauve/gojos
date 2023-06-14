from typing import Dict, Tuple, List
from functools import reduce, partial
from collections import ChainMap

import polars as pl



def explain_df_builder(tournie, explain: Dict):
    series = list(zip(*reduce(partial(_explain_for_team, tournie), explain.items(), [])))
    df = pl.DataFrame({
        'team': series[0],
        'tournament': series[1],
        'draw': series[2],
        'round': series[3],
        'match': series[4],
        'selectedWinner': series[5],
        'selectedSets': series[6],
        'ptsForWinner': series[7],
        'ptsForSets': series[8],
        'ptsForLossMaxSets': series[9]
    }).with_columns([(pl.col('ptsForWinner') + pl.col('ptsForSets') + pl.col('ptsForLossMaxSets')).alias("totalPts")])
    return df


def _explain_for_team(tournie, accum, team_explain: Tuple):
    team, draws = team_explain
    return reduce(partial(_team_and_draw, tournie, team), draws, accum)


def _team_and_draw(tournie, team, accum, draw):
    return reduce(partial(_team_draw_match, tournie, team, draw['event']), draw['matches'], accum)


def _team_draw_match(tournie, team, draw, accum, match) -> List[Tuple]:
    pts = dict(ChainMap(*(match['points'])))
    accum.append((
        team.name,
        tournie.name,
        draw,
        int(match.get('match').split(".")[0]),
        match.get('match', None),
        match.get('selected-winner', None),
        match.get('selected-in-sets', None),
        float(pts.get('correct-winner', None)),
        float(pts.get('correct-sets', None)),
        float(pts.get('bonus-for-loss-in-max-sets', None)),
    ))
    return accum
