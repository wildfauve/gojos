from __future__ import annotations
from functools import partial

from rdflib import URIRef

from gojos import model
from gojos.repo import repository
from gojos import rdf
from gojos.util import fn


class LeaderBoard:
    repo = model.GraphModel(repository.LeaderBoardRepo, model.GraphModel.tournament_graph)

    @classmethod
    def create(cls, event: model.TournamentEvent):
        lb = cls(event=event)
        cls.repo().upsert(lb)
        return lb

    @classmethod
    def load(cls, event: model.TournamentEvent):
        lb = cls.repo().get_by_event_sub(event.subject)
        if not lb:
            return cls.create(event)
        return cls()

    def __init__(self, event: model.TournamentEvent, sub: URIRef = None):
        self.rounds = []
        self.event = event
        self.relative_subject = event.relative_subject + "/Leaderboard"
        self.subject = event.subject + "/Leaderboard" if not sub else sub
        self.player_positions = None
        pass

    def for_round(self, round_number):
        for_round = fn.find(partial(self._round_number_predicate, round_number), self.rounds)
        if not for_round:
            rd = model.Round.create(self, round_number=round_number, previous_rounds=self.rounds)
            self.rounds.append(rd)
            return rd
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

# def tournament_leaderboard(event: model.TournamentEvent, for_round: int):
#     return _add_results(adapter.build_leaderboard(event, for_round)),
#
#
# def _add_results(draws):
#     results = [_round_result(draw, match_blocks) for draw, match_blocks in draws.items()]
#     return results
#
# def _round_result(entries, leaderboard_file, for_round):
#     if not leaderboard_file:
#         return entries
#     py = _results_function()
#     for rd, entries in reduce(partial(_leaderboard_def, for_round), entries, {1: [], 2: [], 3: [], 4: []}).items():
#         if entries:
#             py = py + f"\n\ndef scores(tournie):\n"
#             for entry in entries:
#                 py = py + f"{'':>4}{entry}\n"
#             py = py + f"{'':>4}tournie.leaderboard.for_round({rd}).done()\n"
#
#     _write_file(leaderboard_file, py)
#     return entries
#
#
