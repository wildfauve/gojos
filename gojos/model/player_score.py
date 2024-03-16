from __future__ import annotations
from typing import List, Tuple, Self, Union
from functools import partial
from rdflib import Graph, URIRef, Literal, RDF

from gojos.rdf import rdf_prefix
from gojos.util import fn, tokeniser, monad, singleton, logger
from gojos import model
from gojos.repo import repository
from gojos.players import mens_players


class PlayerScore:
    repo = model.GraphModel(repository.PlayerScoreRepo, model.GraphModel.tournament_graph)

    player_score_cache = []

    @classmethod
    def reset(cls):
        cls.player_score_cache = []
        cls.repo = model.GraphModel(repository.PlayerScoreRepo, model.GraphModel.tournament_graph)

    @classmethod
    def create(cls, player: model.Player, for_round: model.Round, score: int = None, state=None) -> Self:
        if (from_cache := cls.player_from_cache(player)):
            return from_cache.score_for_round(for_round=for_round, score=score, state=state)
        # When this is the first time to see the player
        ps = cls(player=player, leaderboard=for_round.leaderboard, state=state)
        cls.repo().upsert(ps)
        ps.score_for_round(for_round=for_round, score=score)
        cls.player_score_cache.append(ps)
        return ps

    @classmethod
    def load_for_leaderboard(cls, leaderboard: model.LeaderBoard):
        return [cls.build_player_score(leaderboard, ps) for ps in cls.repo().scores_on_leaderboard(leaderboard.subject)]

    @classmethod
    def build_player_score(cls, leaderboard: model.LeaderBoard, player_score: repository.PlayerScore):
        ps = cls(player=None,
                 leaderboard=leaderboard,
                 total=player_score.total,
                 state=model.PlayerState(player_score.state) if player_score.state else None,
                 sub=player_score.subject).build_rounds_from_repo(player_score.round_scores)
        if ps in cls.player_score_cache:
            cls.player_score_cache[cls.player_score_cache.index(ps)] = ps
        else:
            cls.player_score_cache.append(ps)
        return ps

    @classmethod
    def player_from_cache(cls, player):
        if not cls.player_score_cache:
            return None
        return fn.find(partial(cls._player_predicate, player), cls.player_score_cache)

    @classmethod
    def _player_predicate(cls, test_for_player, player_score):
        return test_for_player == player_score.player

    def __init__(self, player: model.Player,
                 leaderboard: model.LeaderBoard,
                 state: model.PlayerState = None,
                 total: int = None,
                 sub: URIRef = None):
        if sub and not player:
            self.player = self.player_from_player_score_sub(sub)
            self.subject = sub
        else:
            self.subject = player.subject + f"/{leaderboard.relative_subject}"
            self.player = player
        self.state = state
        self.leaderboard = leaderboard
        self.rounds = dict()
        self.overall_total = None
        self.round_score = None
        self.current_position = None
        self.total = 0 if not total else total

    def __repr__(self):
        cls_name = self.__class__.__name__
        components = [
            f"player={self.player}",
            f"total={self.total}",
            f"current_position={self.current_position}",
            f"state={self.state}",
            f"round_scores=[{','.join([str(sc['score']) for sc in self.rounds.values()])}]",
            f"round_positions=[{','.join([str(sc['current_pos']) for sc in self.rounds.values()])}]"]
        return f"{cls_name}({', '.join(fn.remove_none(components))})"

    def __hash__(self):
        return hash((self.subject,))

    def __eq__(self, other):
        if not self or not other:
            breakpoint()
        return self.subject == other.subject

    def player_from_player_score_sub(self, player_score_sub) -> model.Player:
        player_sub = URIRef("/".join(player_score_sub.split('/')[0:-3]))
        return model.Player.load(sub=player_sub)

    def build_rounds_from_repo(self, scores: List[repository.RoundScore]):
        for rd in scores:
            self.rounds[rd.round_subject] = self.build_score_dict(rd.score,
                                                                  rd.round_number,
                                                                  rd.running_total,
                                                                  rd.position,
                                                                  model.PlayerState(rd.state) if rd.state else None)

        return self

    def score_for_round(self, for_round: model.Round, score: int, state=None):
        if not score:
            self.rounds[for_round.round_number] = {'score': score, 'current_pos': None}
            return self
        if for_round.subject in self.rounds.keys():
            """
            We are here because we have already added round scores for this player.  
            There maybe a duplicate player.
            """
            breakpoint()
        if state:
            self.state = state
        if score:
            self.total += score
        self.rounds[for_round.subject] = self.build_score_dict(score=score,
                                                               for_round=for_round,
                                                               calc_total=self.total,
                                                               position=None,
                                                               state=self.state)
        self.round_score = score
        self.__class__.repo().add_round_score(self, for_round.subject)
        return self

    def build_score_dict(self,
                         score,
                         for_round: Union[model.Round, int],
                         calc_total,
                         position: int = None,
                         state: model.PlayerState = None):
        return {'score': score,
                'round_number': for_round.round_number if isinstance(for_round, model.Round) else for_round,
                'current_pos': position,
                'running_total': calc_total,
                'state': state}

    def position(self, pos, rd_sub, rd_number: int = None):
        # if self.state:
        #     breakpoint()
        self.current_position = pos
        if not self.rounds.get(rd_sub, None):
            breakpoint()
        if rd_sub:
            self.rounds[rd_sub]['current_pos'] = pos
            self.repo().update_round_position(self, rd_sub, pos)
        return self
