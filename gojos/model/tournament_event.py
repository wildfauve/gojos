from typing import List, Tuple, Dict, Union
from functools import partial, reduce
from itertools import accumulate, pairwise
from enum import Enum

import polars as pl
from rdflib import URIRef
from rich import print

from gojos import model, rdf, fantasy
from gojos.repo import repository
from gojos.util import fn


class PlayerState(Enum):
    CUT = 'cut'
    WD = 'wd'


class TournamentEvent:
    repo = model.GraphModel(repository.TournamentEventRepo, model.GraphModel.tournament_graph)

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
        return [cls.build_event(event[3], event) for event in cls.repo().get_all()]

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
        return cls(event_of=tournament,
                   year=year,
                   cut_strategy=cut_strat,
                   pts_strategy_components=fant_strat,
                   sub=sub)

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
        self.cut_strategy = model.Cut.build(cut_strategy) if not isinstance(cut_strategy, model.Cut) else cut_strategy
        self.errors = []
        self.points_strategy = self.fantasy_strategy(pts_strategy_components)
        self.round_factor_strategy = None
        self.leaderboard = LeaderBoard()
        model.Player.loadall()

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

    def tournament_by_sub(self, sub):
        return model.GrandSlam.get_by_sub(sub)

    def fantasy_strategy(self, components: Union[Tuple, URIRef] = None):
        if components:
            return fantasy.PointsStrategyCalculator.build(components)
        return fantasy.strategy_inverted_position_1_wc_4_max_players_10()

    def add_entries(self, entries):
        self.entries = entries
        self.number_of_entries = len(self.entries)
        return self

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


class LeaderBoard:

    def __init__(self):
        self.rounds = []
        self.player_positions = None
        pass

    def for_round(self, round_number):
        for_round = fn.find(partial(self._round_number_predicate, round_number), self.rounds)
        if not for_round:
            rd = Round(round_number=round_number, previous_rounds=self.rounds)
            self.rounds.append(rd)
            return rd
            # raise error.ConfigException(f"Round id: {round_id} does not exist")
        return for_round

    def _scores_per_player_per_round(self):
        return sorted(reduce(self._player_scores_for_rd, self.rounds, {}).items(), key=lambda r: r[1]['total'])

    def _round_score_dict(self, accum, score_column):
        rd, scores = score_column
        return {**accum, **{f"Round-{rd + 1}": list(scores)}}

    def _transpose_scores(self, scores):
        return enumerate(list(zip(*scores.values())))

    def _player_scores_for_rd(self, accum, for_rd):
        for playerscore in for_rd.players:
            if playerscore.player in accum:
                accum[playerscore.player] = {**accum[playerscore.player],
                                             **{for_rd.round_number: playerscore.round_score}}
                accum[playerscore.player]['total'] = sum(
                    [v for k, v in accum[playerscore.player].items() if isinstance(k, int)])
            else:
                accum[playerscore.player] = {'total': playerscore.round_score,
                                             for_rd.round_number: playerscore.round_score}
        return accum

    def _accumulate(scores):
        return list(accumulate(scores))

    def positions_for_player_per_round(self, player, wildcards):
        return [rd.position_for_player(player, wildcards) for rd in self.rounds]

    def _round_number_predicate(self, number, rd):
        return rd.round_number == number

    def _is_completed(self):
        breakpoint()


class Round:

    def __init__(self, round_number: int, previous_rounds: List):
        self.round_number = round_number
        self.previous_rounds = previous_rounds
        self.players = []

    def done(self):
        """
        Set positions based on round_score
        """
        reduce(self._set_position, self._sort_player_scores(), (1, 0, None))
        return None

    def _sort_player_scores(self):
        return sorted(self._elegible_players(), key=lambda ps: ps.total)

    def _elegible_players(self):
        if self.round_number < 3:
            return self.players
        return [p for p in self.players if not p.player_state]

    def position_for_player(self, player, wildcards):
        player_scr = fn.find(partial(self._player_predicate, self._player_or_wildcard(player, wildcards)), self.players)
        if not player_scr:
            breakpoint()
        return player_scr.rounds[self.round_number]['current_pos']

    def player(self, pl):
        ps = model.PlayerScore.scoring_for_player(player=pl, round_number=self.round_number)
        self.players.append(ps)
        return ps

    def _set_position(self, accum, player_score):
        pos, at_same_pos, current_score = accum

        if not current_score:
            player_score.position(pos, self.round_number)
            return (pos, at_same_pos, player_score.total)

        if player_score.total == current_score:
            player_score.position(pos, self.round_number)
            return (pos, at_same_pos + 1, current_score)

        new_pos = pos + (1 + at_same_pos)
        player_score.position(new_pos, self.round_number)
        return (new_pos, 0, player_score.total)

    def _player_score_from_this_and_previous(self, player_score, previous_rds):
        if not previous_rds:
            return player_score.round_score
        previous_scores = [self._find_player_score_in_round(player_score, previous) for previous in previous_rds]
        return sum(previous_scores + [player_score.round_score])

    def _find_player_score_in_round(self, player_score, for_round):
        ps = fn.find(partial(self._player_predicate, player_score.player), for_round.players)
        if not ps:
            breakpoint()
        return ps.round_score

    def _player_or_wildcard(self, player, wildcards):
        wc = model.WildCard.has_swap(wildcards, player, self.round_number)
        if wc:
            print(
                f"Round: {self.round_number} Trade out [bold blue]{player.klass_name}[/] trade in [bold green]{wc.trade_in_player.klass_name}")
            return wc.trade_in_player
        return player

    def _player_predicate(self, for_player, player_score):
        return for_player == player_score.player
