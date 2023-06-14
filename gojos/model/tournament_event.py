from typing import List
from functools import partial
from itertools import accumulate

from gojos.util import fn


class TournamentEvent:

    def __init__(self, event_of, year):
        self.is_event_of = event_of
        self.scheduled_in_year = year
        self.name = f"{self.is_event_of.subject_name}{self.scheduled_in_year}"
        self.label = f"{self.is_event_of.name} {self.scheduled_in_year}"
        self.entries = []
        self.rounds = []
        self.errors = []
        self.points_strategy = None
        self.round_factor_strategy = None
        self.leaderboard = LeaderBoard()

    def add_entries(self, entries):
        self.entries = entries
        return self

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

    def for_round(self, rd):
        rd = fn.find(partial(self._round_number_predicate, rd), self.rounds)
        if not rd:
            rd = Round(rd=rd)
            self.rounds.append(rd)
            # raise error.ConfigException(f"Round id: {round_id} does not exist")
        return rd

    def _round_number_predicate(self, number, rd):
        return rd.rd == number


class Round:

    def __init__(self, rd: int):
        self.rd = rd
        self.players = []

    def player(self, plyr):
        ps = PlayerScore(player=plyr)
        self.players.append(ps)
        return ps


class PlayerScore:

    def __init__(self, player):
        self.player = player
        self.score = None

    def score(self, scr):
        self.score = scr
        return self

