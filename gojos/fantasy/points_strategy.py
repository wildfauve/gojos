from typing import Callable, List, Tuple, Union, Type, Optional, Dict
from functools import reduce
from enum import Enum
from collections import ChainMap

from gojos import model


class Points521(Enum):
    NO_POINTS = ('', 0)
    WINNER = ('correct-winner', 5)
    NUMBER_OF_SETS = ('correct-sets', 2)
    LOST_WITH_MAX_SETS = ('bonus-for-loss-in-max-sets', 1)


class Points1HalfHalf(Enum):
    NO_POINTS = ('', 0)
    WINNER = ('correct-winner', 1)
    NUMBER_OF_SETS = ('correct-sets', 0.5)
    LOST_WITH_MAX_SETS = ('bonus-for-loss-in-max-sets', 0.5)


class Points21Half(Enum):
    NO_POINTS = ('', 0)
    WINNER = ('correct-winner', 2)
    NUMBER_OF_SETS = ('correct-sets', 1)
    LOST_WITH_MAX_SETS = ('bonus-for-loss-in-max-sets', 0.5)


class PointsStrategyCalculator:

    def __init__(self, pts_strategy: Union[Type[Points521], Type[Points1HalfHalf]],
                 per_round_accum_strategy: Callable):
        self.pts_strategy = pts_strategy
        self.per_round_accum_strategy = per_round_accum_strategy


class WinNumSetsLossMaxSets(PointsStrategyCalculator):
    """
    Strategy for calculating Fantasy Points.
    + n points for selecting the correct winner
    + n points for selecting the correct number of sets
    + n points for not selecting the correct winner, but getting the sets correct.
    """

    def explain_points_for_round(self, for_round):
        w = self._points_with_factor(self.pts_strategy.WINNER.value[1], for_round)
        s = self._points_with_factor(self.pts_strategy.NUMBER_OF_SETS.value[1], for_round)
        ls = self._points_with_factor(self.pts_strategy.LOST_WITH_MAX_SETS.value[1], for_round)
        return f"w({w}) s({s}) lms({ls})"

    def calc(self, selection: model.Selection, explain: bool = False) -> Union[int, Dict]:
        result = [strategy(selection, explain) for strategy in self.points_strategy_fns()]
        if explain:
            return result
        return sum(result)

    def points_strategy_fns(self) -> List[Callable]:
        return [self.selected_correct_winner, self.selected_correct_sets, self.lost_but_in_max_sets]

    def selected_correct_winner(self, selection: model.Selection, explain: bool = False) -> int:
        if selection.match.match_winner == selection.selected_winner:
            return self._calc(self.pts_strategy.WINNER,
                              selection.round_id,
                              explain)
        return self._calc(self.pts_strategy.NO_POINTS,
                          selection.round_id,
                          explain,
                          self.pts_strategy.WINNER)

    def selected_correct_sets(self, selection: model.Selection, explain: bool = False) -> int:
        if selection.match.match_winner != selection.selected_winner:
            return self._calc(self.pts_strategy.NO_POINTS,
                              selection.round_id,
                              explain,
                              self.pts_strategy.NUMBER_OF_SETS)
        if selection.in_number_sets == selection.match.number_of_sets_played():
            return self._calc(self.pts_strategy.NUMBER_OF_SETS,
                              selection.round_id,
                              explain)
        return self._calc(self.pts_strategy.NO_POINTS,
                          selection.round_id,
                          explain,
                          self.pts_strategy.NUMBER_OF_SETS)

    def lost_but_in_max_sets(self, selection: model.Selection, explain: bool = False) -> int:
        if ((selection.match.match_winner != selection.selected_winner) and
            selection.match.max_sets_played()):
                # selection.match.number_of_sets_played() == selection.in_number_sets):
            return self._calc(self.pts_strategy.LOST_WITH_MAX_SETS,
                              selection.round_id,
                              explain)
        return self._calc(self.pts_strategy.NO_POINTS,
                          selection.round_id,
                          explain,
                          self.pts_strategy.LOST_WITH_MAX_SETS)

    def _calc(self,
              points_type: Union[Points521, Points1HalfHalf],
              rd: int,
              explain: bool = False,
              when_no_points: Union[Points521, Points1HalfHalf] = None) -> Union[int, Dict]:
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


def doubling_per_round_strategy(rd: int):
    if rd == 1:
        return 1
    return 2 ** (rd - 1)


def strategy_1_point5_point5_double():
    return WinNumSetsLossMaxSets(Points1HalfHalf, doubling_per_round_strategy)


def strategy_5_2_1_double():
    return WinNumSetsLossMaxSets(Points521, doubling_per_round_strategy)


def strategy_2_1_point5_double():
    return WinNumSetsLossMaxSets(Points21Half, doubling_per_round_strategy)


def points_list_to_dict(points: List[Dict[str, int]]):
    return dict(ChainMap(*points))
