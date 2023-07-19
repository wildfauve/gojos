from typing import List, Tuple, Dict, Union, Optional
from functools import partial, reduce
from itertools import accumulate, pairwise
from enum import Enum

import polars as pl
from rdflib import URIRef
from rich import print

from gojos import model, rdf, fantasy, adapter
from gojos.repo import repository
from gojos.util import fn


class PlayerState(Enum):
    CUT = 'urn:clojos:golf:playerState:cut'
    WD = 'urn:clojos:golf:playerState:withDrawn'


class TournamentEvent:
    repo = model.GraphModel(repository.TournamentEventRepo, model.GraphModel.tournament_graph)

    @classmethod
    def reset(cls):
        cls.repo = model.GraphModel(repository.TournamentEventRepo, model.GraphModel.tournament_graph)

    @classmethod
    def create(cls,
               year: int,
               tournament_name: str = None,
               tournament=None,
               cut_strategy: str = None):
        event_of = tournament if isinstance(tournament, model.GrandSlam) else model.GrandSlam.get(name=tournament_name)
        event = cls(event_of=event_of, year=year, cut_strategy=cut_strategy)
        cls.repo().upsert(event)
        return event

    @classmethod
    def get_all(cls):
        # The tournament URI is the last value in the array
        return [cls.build_event(event[-1], event) for event in cls.repo().get_all()]

    @classmethod
    def get(cls, year: int, tournament):
        event = cls.repo().find_by_year(tournament.subject, year)
        if not event:
            return None
        return cls.build_event(tournament, event)

    @classmethod
    def get_all_for_tournament(cls, tournament):
        return [cls.build_event(tournament, event) for event in cls.repo().find_by_tournament(tournament.subject)]

    @classmethod
    def build_event(cls, tournament: Union[model.Tournament, str, URIRef], event):
        year, name, sub, cut_strat, fant_strat, _tourn_sub = event
        ev = cls(event_of=tournament,
                 year=year,
                 cut_strategy=cut_strat,
                 pts_strategy_components=fant_strat,
                 sub=sub)
        ev.load_entries()
        return ev

    @classmethod
    def get_by_sub(cls, sub):
        event = cls.repository().get_by_sub(sub)
        if not event:
            return None
        return cls(*[event[-1:][0]] + list(event[:-1]))

    def __init__(self,
                 event_of,
                 year,
                 pts_strategy_components: Union[tuple, URIRef] = None,
                 cut_strategy: Union[str, URIRef, model.Cut] = None,
                 sub: URIRef = None):
        if isinstance(event_of, model.GrandSlam):
            self.is_event_of = event_of
        elif isinstance(event_of, URIRef):
            self.is_event_of = self.tournament_by_sub(event_of)
        else:
            self.is_event_of = self.tournament_by_sub(event_of)
        self.scheduled_in_year = year
        self.name = f"{self.is_event_of.subject_name}{self.scheduled_in_year}"
        self.relative_subject = f"{self.is_event_of.subject_name}/{self.scheduled_in_year}"
        self.label = f"{self.is_event_of.name} {self.scheduled_in_year}"
        self.subject = rdf.clo_go_ind_tou[self.relative_subject] if not sub else sub
        self.entries = []
        self.number_of_entries = None
        self.rounds = []
        self.course = None
        self.cut_strategy = self.build_cut_strategy(cut_strategy)
        self.errors = []
        self.points_strategy = self.fantasy_strategy(pts_strategy_components)
        self.round_factor_strategy = None
        self.leaderboard = None

    def __repr__(self):
        cls_name = self.__class__.__name__
        components = [
            f"name={self.name}",
            f"label={self.label}",
            f"number_of_entries={self.number_of_entries}"]
        return f"{cls_name}({', '.join(fn.remove_none(components))})"

    def __hash__(self):
        return hash((self.subject,))

    def __eq__(self, other):
        if not self or not other:
            return None
        return self.subject == other.subject

    def load(self):
        """
        Load object graph from persisted triples.
        Add players to the player module.
        :return:
        """

        model.Player.loadall()
        self.leaderboard = model.LeaderBoard.load(self)
        self.load_entries()
        return self

    def load_entries(self):
        self.add_entries([model.Player.load(sub=sub) for sub in self.__class__.repo().get_entries(self.subject)])
        return self

    def scores_for_round(self, for_round: int):
        self.leaderboard.for_round(for_round).upsert_scores()
        return self

    def build_entry_list(self):
        self.add_entries([scrapped_player.player_klass for scrapped_player in adapter.build_leaderboard(for_round=1)])
        return self

    def tournament_by_sub(self, sub):
        return model.GrandSlam.get_by_sub(sub)

    def build_cut_strategy(self, cut_strategy: Optional[Union[model.Cut, str]] = None):
        if not cut_strategy:
            return model.CutTop60AndTies()
        return model.Cut.build(cut_strategy) if not isinstance(cut_strategy, model.Cut) else cut_strategy

    def fantasy_strategy(self, components: Union[Tuple, URIRef] = None):
        if components:
            return fantasy.PointsStrategyCalculator.build(components)
        return fantasy.strategy_inverted_position_1_wc_4_max_players_10()

    def add_entries(self, entries: List[Union[str, model.Player]]):
        [self.add_entry(entry) for entry in entries]
        self.number_of_entries = len(self.entries)
        return self

    def add_entry(self, player_klass_name_or_klass: Union[str, model.Player]):
        player = model.Player.load(klass_name=player_klass_name_or_klass) if isinstance(player_klass_name_or_klass,
                                                                                        str) else player_klass_name_or_klass
        if not self.is_player_entered(player):
            self.__class__.repo().add_player_as_entry(self, player)
            self.entries.append(player)
        return self

    def is_player_entered(self, player) -> bool:
        return player in self.entries

    def at_course(self, course):
        self.course = course
        return self

    def has_cut_strategy(self, strategy):
        self.cut_strategy = strategy
        return self

    def positions_for_player_per_round(self, player, wildcards: List = []):
        return self.leaderboard.positions_for_player_per_round(player, wildcards)

    def relative_to_cut(self, player):
        return self.cut_strategy.relative_to_cut(self.positions_for_player_per_round(player)[-1])

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
