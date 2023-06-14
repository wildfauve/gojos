import polars as pl

from gojos.util import echo


def to_parquet(file, df: pl.DataFrame):
    df.write_parquet(file)
    echo.echo(f"File written to {file}")
    pass