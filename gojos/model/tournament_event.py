from typing import List
from functools import partial
from itertools import accumulate

from gojos.model import fantasy
from gojos.util import fn


class TournamentEvent:

    def __init__(self, event_of, year):
        self.is_event_of = event_of
        self.scheduled_in_year = year
        self.name = f"{self.is_event_of.subject_name}{self.scheduled_in_year}"
        self.label = f"{self.is_event_of.name} {self.scheduled_in_year}"
        self.entries = []
        self.number_of_entries = None
        self.rounds = []
        self.course = None
        self.errors = []
        self.points_strategy = None
        self.round_factor_strategy = None
        self.leaderboard = LeaderBoard()

    def add_entries(self, entries):
        self.entries = entries
        self.number_of_entries = len(self.entries)
        return self

    def at_course(self, course):
        self.course = course
        return self

    def positions_for_player_per_round(self, player, wildcards):
        return self.leaderboard.positions_for_player_per_round(player, wildcards)

    def fantasy_points_strategy(self, points_strategy):
        self.points_strategy = points_strategy
        return self

    def fantasy_round_points_accum_strategy(self, accum_strat):
        self.round_factor_strategy = accum_strat
        return self

    def fantasy_points_schedule(self, rd_number, accum: bool = False) -> List:
        sched = [len(self.draws) * pt for pt in (self.draws[0].fantasy_points_schedule(rd_number))]
        if not accum:
            return sched
        return list(accumulate(sched))

    def fantasy_points_allocation(self, rd_number: int) -> str:
        return self.draws[0].fantasy_points_allocation(rd_number)


class LeaderBoard:

    def __init__(self):
        self.rounds = []
        pass

    def for_round(self, round_number):
        for_round = fn.find(partial(self._round_number_predicate, round_number), self.rounds)
        if not for_round:
            rd = Round(round_number=round_number)
            self.rounds.append(rd)
            return rd
            # raise error.ConfigException(f"Round id: {round_id} does not exist")
        return for_round

    def positions_for_player_per_round(self, player, wildcards):
        return [rd.position_for_player(player, wildcards) for rd in self.rounds]

    def _round_number_predicate(self, number, rd):
        return rd.round_number == number


class Round:

    def __init__(self, round_number: int):
        self.round_number = round_number
        self.players = []

    def position_for_player(self, player, wildcards):
        player_scr = fn.find(partial(self._player_predicate, self._player_or_wildcard(player, wildcards)), self.players)
        if not player_scr:
            breakpoint()
        return player_scr.round_position

    def player(self, plyr):
        ps = PlayerScore(player=plyr)
        self.players.append(ps)
        return ps

    def _player_or_wildcard(self, player, wildcards):
        wc = fantasy.WildCard.has_swap(wildcards, player, self.round_number)
        if wc:
            return wc.trade_in_player
        return player

    def _player_predicate(self, for_player, player_score):
        return for_player == player_score.player


class PlayerScore:

    def __init__(self, player):
        self.player = player
        self.round_score = None
        self.round_position = None

    def score(self, scr):
        self.round_score = scr
        return self

    def position(self, pos):
        self.round_position = pos
        return self
