import polars as pl


def sum_races(df, race_columns) -> pl.DataFrame:
    return df.select(pl.col('team'), _sum_fold(race_columns))


def filter_team_name(df, team_name) -> pl.DataFrame:
    return df.filter(pl.col('team') == team_name)


def rankings(df, rank_columns):
    return df.with_columns([_rank_defn(col) for col in rank_columns])


def _rank_defn(col):
    return pl.col(col).rank('ordinal', descending=True).alias(f"{col}_rank")


def _sum_fold(columns):
    return pl.fold(acc=pl.lit(0), f=lambda acc, x: acc + x, exprs=pl.col(columns).alias("sum"))
