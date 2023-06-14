from typing import List, Tuple

from rich.table import Table
import polars as pl

from gojos.adapter import discord

from . import console


def plot_to_channel(file: str, channel: bool):
    if channel == "to-discord":
        _send_to_discord(file)
    pass


def _send_to_discord(file):
    discord.send_attachment(msg_title="Fantasy Plot",
                            file_path=file,
                            description="Rankings",
                            file_name="plot.png")
    pass
