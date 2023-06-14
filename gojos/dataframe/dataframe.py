import polars as pl

from .expr import rankings


def build_df(team_scores, sort: bool = True) -> pl.DataFrame:
    df = pl.DataFrame(team_scores)
    if not sort:
        return df
    return df.sort(df.columns[-1], descending=True)


def round_rank(df) -> pl.DataFrame:
    cols = df.columns[1:]
    return rankings(df, cols).drop(cols)

