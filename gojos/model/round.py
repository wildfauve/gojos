from __future__ import annotations
from typing import List, Tuple, Optional
from functools import partial, reduce

from rdflib import URIRef

from gojos import model, adapter
from gojos.repo import repository
from gojos.util import fn, logger


class Round:
    repo = model.GraphModel(repository.RoundRepo, model.GraphModel.tournament_graph)

    @classmethod
    def reset(cls):
        cls.repo = model.GraphModel(repository.RoundRepo, model.GraphModel.tournament_graph)

    @classmethod
    def create(cls, leaderboard: model.LeaderBoard, round_number: int, ):
        rd = cls(leaderboard=leaderboard, round_number=round_number)
        cls.repo().upsert(rd)
        return rd

    @classmethod
    def load_for_leaderboard(cls, leaderboard: model.LeaderBoard):
        return [cls.build_round(leaderboard, rd) for rd in sorted(cls.repo().get_all(leaderboard.subject),
                                                                  key=lambda rd: rd[1])]

    @classmethod
    def build_round(cls, leaderboard: model.LeaderBoard, rd: Tuple):
        sub, number = rd
        return cls(leaderboard=leaderboard, round_number=number, sub=sub)

    def __init__(self, leaderboard: model.LeaderBoard, round_number: int, sub: URIRef = None):
        self.round_number = round_number
        self.leaderboard = leaderboard
        self.subject = leaderboard.subject + f"/Round/{self.round_number}" if not sub else sub
        self.player_scores = []

    def __repr__(self):
        cls_name = self.__class__.__name__
        components = [
            f"round_number={self.round_number}"]
        return f"{cls_name}({', '.join(fn.remove_none(components))})"

    def upsert_scores(self):
        [self.apply_scraped_player_score(scrap) for scrap in adapter.build_leaderboard(for_round=self.round_number)]
        self.done()
        return self

    def apply_scraped_player_score(self, scrapped_player: adapter.ScrappedPlayer):
        if (len(scrapped_player.round_scores) < self.round_number
                or not scrapped_player.round_scores):
            # or not scrapped_player.round_scores[self.round_number]):
            breakpoint()
        rd_score = int(scr) if (scr := scrapped_player.round_scores.get(self.round_number, None)) else None
        self.player_score(scrapped_player.player_klass,
                          rd_score,
                          state=scrapped_player.player_state)

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
        return [p for p in self.player_scores if not p.state]

    def position_for_player(self, player: model.Player, wildcards: List[model.WildCard]):
        player_or_wc = self._player_or_wildcard(player, wildcards)
        player_scr = fn.find(partial(self._player_predicate, player_or_wc), self.player_scores)
        if not player_scr:
            breakpoint()
        if self.subject not in player_scr.rounds:
            return model.PlayerState.CUT

        # return player_scr.rounds[self.subject]['current_pos']
        return {**player_scr.rounds[self.subject], **{'player': player_or_wc}}

    def load_player_scores(self, player_scores: model.Player):
        self.player_scores = player_scores
        return self

    def scores_for_player(self, player: model.Player) -> model.PlayerScore:
        return fn.find(lambda ps: ps.player == player, self.player_scores)

    def player_score(self, player: model.Player, score: int = None, state: Optional[model.PlayerState] = None):
        if not score and state == model.PlayerState.CUT:  # that is, they missed the cut
            return self
        if not score:
            breakpoint()
        ps = model.PlayerScore.create(player=player, for_round=self, score=score, state=state)
        if self.round_number == 1:  # That is, the first time this player has set a score; usually round 1
            self.leaderboard.add_scoring_player(ps.subject)
        self.player_scores.append(ps)
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
            logger.debug(
                f"Round: {self.round_number} Trade out [bold blue]{player.klass_name}[/] trade in [bold green]{wc.trade_in_player.klass_name}")
            return wc.trade_in_player
        return player

    def _player_predicate(self, for_player, player_score):
        return for_player == player_score.player
