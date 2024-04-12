import polars as pl


def sum_rounds(df, round_columns) -> pl.DataFrame:
    return df.select(pl.col('Player'), _sum_fold(round_columns))


def add_rd_total(df, round_columns) -> pl.DataFrame:
    return df.with_columns([_sum_fold(round_columns)])


def add_total_column(df, round_columns) -> pl.DataFrame:
    return df.with_columns([_sum_fold(round_columns)])


def filter_team_name(df, team_name) -> pl.DataFrame:
    return df.filter(pl.col('team') == team_name)


def rankings(df, rank_columns):
    return df.with_columns([_rank_defn(col) for col in rank_columns])


def _rank_defn(col):
    return pl.col(col).rank('ordinal', descending=True).alias(f"{col}_rank")


def _sum_fold(columns):
    return pl.fold(acc=pl.lit(0), function=lambda acc, x: acc + x, exprs=pl.col(columns).alias("Total"))
