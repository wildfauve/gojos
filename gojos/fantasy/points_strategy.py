from typing import Callable, List, Tuple, Union, Type, Optional, Dict
from functools import reduce
from enum import Enum
from collections import ChainMap
import sys

from rdflib import URIRef

from gojos import model, rdf


class Points1_4_10(Enum):
    POINTS_PER_POSITION = 1
    POINTS_FOR_MISSED_CUT = 0
    MAX_WILDCARD = 4
    MAX_PLAYERS = 10


class Points1_2_4(Enum):
    """
    Class for testing only.
    """
    POINTS_PER_POSITION = 1
    POINTS_FOR_MISSED_CUT = 0
    MAX_WILDCARD = 2
    MAX_PLAYERS = 4


class PointsStrategyCalculator:

    @classmethod
    def build(cls, sub: Union[URIRef, Tuple]):
        if isinstance(sub, tuple):
            klass_name, pts_strat_name = sub
        else:
            klass_name, pts_strat_name = sub.split("/")[-2:]
        klass = getattr(sys.modules[__name__], klass_name)
        strat_klass = getattr(sys.modules[__name__], pts_strat_name)
        return klass(strat_klass)

    def __init__(self, pts_strategy: Union[Type[Points1_4_10], Type[Points1_2_4]]):
        self.pts_strategy = pts_strategy


    def subject(self):
        return URIRef(
            rdf.FANTASY_POINTS_STRATEGY) + f"/{self.__class__.__name__}/{self.pts_strategy.__name__}"


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
                roster_player.event.positions_for_player_per_round(roster_player.player, wildcards)]

    def _invert_position(self, roster_player, pos):
        if isinstance(pos, model.PlayerState) or not pos:
            return self.pts_strategy.POINTS_FOR_MISSED_CUT.value
        return self._points_with_factor(roster_player.event.number_of_entries + 1 - pos)

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
