from __future__ import annotations
from typing import List
from functools import partial, reduce

from rdflib import URIRef

from gojos import model, adapter
from gojos.repo import repository
from gojos.util import fn


class Round:
    repo = model.GraphModel(repository.RoundRepo, model.GraphModel.tournament_graph)

    @classmethod
    def reset(cls):
        cls.repo = model.GraphModel(repository.RoundRepo, model.GraphModel.tournament_graph)

    @classmethod
    def create(cls, leaderboard: model.LeaderBoard, round_number: int, previous_rounds: List[model.Round]):
        rd = cls(leaderboard=leaderboard, round_number=round_number, previous_rounds=previous_rounds)
        cls.repo().upsert(rd)
        return rd

    def __init__(self, leaderboard: model.LeaderBoard, round_number: int, previous_rounds: List, sub: URIRef = None):
        self.round_number = round_number
        self.previous_rounds = previous_rounds
        self.leaderboard = leaderboard
        self.subject = leaderboard.subject + f"/Round/{self.round_number}" if not sub else sub
        self.player_scores = []

    def __repr__(self):
        cls_name = self.__class__.__name__
        components = [
            f"round_number={self.round_number}"]
        return f"{cls_name}({', '.join(fn.remove_none(components))})"

    def upsert_scores(self):
        [self.player_score(scrapped_player.player_klass, int(scrapped_player.round_scores[0])) for scrapped_player in
         adapter.build_leaderboard(for_round=self.round_number)]
        self.done()
        return self

    def done(self):
        """
        Set positions based on round_score
        """
        reduce(self._set_position, self._sort_player_scores(), (1, 0, None))
        return None

    def _sort_player_scores(self):
        return sorted(self._eligible_players(), key=lambda ps: ps.total)

    def _eligible_players(self):
        if self.round_number < 3:
            return self.player_scores
        return [p for p in self.player_scores if not p.player_state]

    def position_for_player(self, player: model.Player, wildcards: List[model.WildCard]):
        player_scr = fn.find(partial(self._player_predicate, self._player_or_wildcard(player, wildcards)),
                             self.player_scores)
        if not player_scr:
            breakpoint()
        return player_scr.rounds[self.subject]['current_pos']

    def player_score(self, player: model.Player, score: int):
        score = model.PlayerScore.create(player=player, for_round=self, score=score)
        # if self.round_number > 1:
        #     breakpoint()
        self.player_scores.append(score)
        return self

    def _set_position(self, accum, player_score):
        pos, at_same_pos, current_score = accum

        if not current_score:
            player_score.position(pos, self.subject, self.round_number)
            return (pos, at_same_pos, player_score.total)

        if player_score.total == current_score:
            player_score.position(pos, self.subject, self.round_number)
            return (pos, at_same_pos + 1, current_score)

        new_pos = pos + (1 + at_same_pos)
        player_score.position(new_pos, self.subject, self.round_number)
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
