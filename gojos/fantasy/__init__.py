from .year_2023 import uo as uo_2023
from .year_2023 import to as to_2023

fantasy_tournaments = {
    "USOpen2023": uo_2023,
    "TheOpen2023": to_2023
}

from .points_strategy import (
    InvertedPosition,
    PointsStrategyCalculator,
    strategy_inverted_position_1_wc_4_max_players_10
)
