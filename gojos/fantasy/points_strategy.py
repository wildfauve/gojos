from typing import Callable, List, Tuple, Union, Type, Optional, Dict
from functools import reduce
from enum import Enum
from collections import ChainMap

from gojos import model


class Points1_4_10(Enum):
    POINTS_PER_POSITION = 1
    MAX_WILDCARD = 4
    MAX_PLAYERS = 10


class Points1_2_4(Enum):
    """
    Class for testing only.
    """
    POINTS_PER_POSITION = 1
    MAX_WILDCARD = 2
    MAX_PLAYERS = 4


class PointsStrategyCalculator:

    def __init__(self, pts_strategy: Union[Type[Points1_4_10]]):
        self.pts_strategy = pts_strategy


class InvertedPosition(PointsStrategyCalculator):
    """
    """

    def valid_wildcard(self, wildcards, _new_wildcard):
        return len(wildcards) < self.pts_strategy.MAX_WILDCARD.value

    def valid_for_roster(self, roster, _new_player):
        return len(roster) < self.pts_strategy.MAX_PLAYERS.value

    def calc(self, roster_player: model.RosterPlayer, wildcards, explain: bool = False) -> Union[int, List]:
        return self._one_pt_per_inverted_position(roster_player, wildcards, explain)

    def _one_pt_per_inverted_position(self, roster_player: model.RosterPlayer, wildcards, explain: bool = False) -> List[int]:
        return [self._invert_position(roster_player, pos) for pos in
                roster_player.tournament.positions_for_player_per_round(roster_player.player, wildcards)]

    def _invert_position(self, roster_player, pos):
        if isinstance(pos, model.PlayerState):
            return 0
        return self._points_with_factor(roster_player.tournament.number_of_entries + 1 - pos)

    def _points_with_factor(self, points: int) -> int:
        return points * self.pts_strategy.POINTS_PER_POSITION.value

    def calc_points_schedule(self, number_of_matches: int) -> List[int]:
        round_of = self._max_number_rds(number_of_matches)
        return reduce(self._points_schedule_for_rd, zip(round_of, range(1, len(round_of) + 1)), [])

    def _points_schedule_for_rd(self,
                                acc: List[Optional[int]],
                                rd_match_numbers: Tuple[int, int]):
        num_matches, rd = rd_match_numbers
        pts = self.per_round_accum_strategy(rd) * (sum([pts for _name, pts in self._points_of_type()]) * num_matches)
        acc.append(pts)
        return acc

    def _points_of_type(self) -> List[Callable]:
        return [self.pts_strategy.WINNER.value,
                self.pts_strategy.NUMBER_OF_SETS.value]

    def _max_number_rds(self, number_of_matches: int) -> List[int]:
        return self._rd_range([], number_of_matches)

    def _rd_range(self, acc: List[Optional[int]], curr: int) -> List[int]:
        if curr < 1:
            return acc
        acc.append(curr)
        return self._rd_range(acc, int(curr / 2))


def strategy_inverted_position_1_wc_4_max_players_10():
    return InvertedPosition(Points1_4_10)


def strategy_inverted_position_1_wc_2_max_players_4():
    """
    for testing only
    """
    return InvertedPosition(Points1_2_4)


def points_list_to_dict(points: List[Dict[str, int]]):
    return dict(ChainMap(*points))
