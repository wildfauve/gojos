from typing import Callable, List, Tuple, Union, Type, Optional, Dict
from functools import reduce
from enum import Enum
from collections import ChainMap

from gojos import model


class Points1(Enum):
    POINTS_PER_POSITION = ('position', 1)


class PointsStrategyCalculator:

    def __init__(self, pts_strategy: Union[Type[Points1]]):
        self.pts_strategy = pts_strategy


class InvertedPosition1Position4wildcards(PointsStrategyCalculator):
    """
    """

    def calc(self, selection: model.Selection, explain: bool = False) -> Union[int, Dict]:
        return self._one_pt_per_inverted_position(selection, explain)

    # def _points_strategy_fns(self) -> List[Callable]:
    #     return [self._one_pt_per_inverted_position]

    def _one_pt_per_inverted_position(self, selection: model.Selection, explain: bool = False) -> int:
        return [self._invert_position(selection, pos) for pos in
                selection.tournament.positions_for_player_per_round(selection.player)]

    def _invert_position(self, selection, pos):
        return selection.tournament.number_of_entries + 1 - pos

    def _calc(self,
              points_type,
              rd: int,
              explain: bool = False) -> Union[int, Dict]:
        points_name, value = points_type.value
        if points_type == self.pts_strategy.NO_POINTS:
            return value if not explain else {when_no_points.value[0]: value}
        return self._points_with_factor(value, rd) if not explain else {
            points_name: self._points_with_factor(value, rd)}

    def _points_with_factor(self, points: int, rd: int) -> int:
        return points * self.per_round_accum_strategy(rd)

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


def strategy_inverted_position_1_per_position_4_wildcards():
    return InvertedPosition1Position4wildcards(Points1)


def points_list_to_dict(points: List[Dict[str, int]]):
    return dict(ChainMap(*points))
