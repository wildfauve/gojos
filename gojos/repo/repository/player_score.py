from __future__ import annotations
from typing import Tuple, List, NamedTuple
from functools import partial
from itertools import groupby
# from collections import namedtuple

from rdflib import Graph, URIRef, Literal, RDF, BNode

from gojos import rdf, model
from gojos.util import fn, logger

from . import graphrepo


RoundScore = NamedTuple('RoundScore', [('round_number', int),
                                       ('score', int),
                                       ("position", int),
                                       ('running_total', int),
                                       ('state', str),
                                       ('round_subject', URIRef)])
PlayerScore = NamedTuple('PlayerScore', [('subject', URIRef),
                                         ('total', int),
                                         ('position', int),
                                         ('state', str),
                                         ('round_scores', RoundScore)])


def add_round_score(g, score: model.PlayerScore, rd_sub: URIRef.Round):
    breakpoint()
    if score.state:
        g.set((score.subject, rdf.playerIsInState, Literal(score.state.value)))
    g.set((score.subject, rdf.hasScoreTotal, Literal(score.total)))
    create_round_bnode(g, score.subject, rd_sub, score.rounds[rd_sub])

def create_round_bnode(g, sub, round_sub, score_for_round):
    bn = BNode()
    g.add((bn, rdf.isRoundSubject, round_sub))
    g.add((bn, rdf.isRoundNumber, Literal(score_for_round['round_number'])))
    g.add((bn, rdf.hasRoundScore, Literal(score_for_round['score'])))
    if (pos := score_for_round['current_pos']):
        g.add((bn, rdf.hasPositionAfterRound, Literal(pos)))

    if (state:=score_for_round['state']):
        g.add((bn, rdf.playerIsInState, Literal(score_for_round['state'].value)))
    g.add((bn, rdf.hasRunningScoreTotal, Literal(score_for_round['running_total'])))
    g.add((sub, rdf.hasRoundScores, bn))


class PlayerScoreRepo(graphrepo.GraphRepo):
    rdf_type = rdf.PLAYER_SCORE

    def __init__(self, graph: Graph):
        self.graph = graph

    def upsert(self, player_score):
        rdf.subject_finder_creator(self.graph,
                                   player_score.subject,
                                   self.rdf_type,
                                   partial(self.creator, player_score),
                                   partial(self.updater, player_score))
        pass

    def updater(self, score: model.PlayerScore, sub):
        breakpoint()

    def creator(self, score: model.PlayerScore, g, sub):
        g.add((sub, RDF.type, rdf.PLAYER_SCORE))
        g.add((sub, rdf.isOnLeaderboard, score.leaderboard.subject))
        if (pos := score.current_position):
            g.add((sub, rdf.isInCurrentPosition, Literal(pos)))
        [self.create_round_bnode(g, sub, round_sub, round_score) for round_sub, round_score in score.rounds.items()]
        return g

    def add_round_score(self, score: model.PlayerScore, rd_sub: URIRef.Round):
        if score.state:
            self.graph.set((score.subject, rdf.playerIsInState, Literal(score.state.value)))
        self.graph.set((score.subject, rdf.hasScoreTotal, Literal(score.total)))
        self.create_round_bnode(self.graph, score.subject, rd_sub, score.rounds[rd_sub])

    def scores_on_leaderboard(self, lb_sub: URIRef):
        return self.query_for_all_scores(lb_sub, perf_ctx=lb_sub)


    @logger.with_perf_log(name="PlayerScore.query_for_all_scores")
    def query_for_all_scores(self, lb_sub, perf_ctx):
        return [self.load_player_score(ps) for ps in
                rdf.all_matching(self.graph, (None, rdf.isOnLeaderboard, lb_sub), form=rdf.subject)]



    def load_player_score(self, sub):
        triples = rdf.all_matching(self.graph, (sub, None, None))
        total = rdf.triple_finder(rdf.hasScoreTotal, triples)
        pos = rdf.triple_finder(rdf.isInCurrentPosition, triples)
        state = rdf.triple_finder(rdf.playerIsInState, triples)
        rd_scores = [self.load_rd_bnodes(bn) for bn in
                     rdf.triple_finder(rdf.hasRoundScores, triples, filter_fn=fn.select, builder=rdf.all_objects)]
        return PlayerScore(sub,
                           total.toPython(),
                           pos.toPython(),
                           state.toPython() if state else None,
                           rd_scores)

    def load_rd_bnodes(self, bn_sub):
        """
        [ clo-go:hasPositionAfterRound 3 ;
            clo-go:hasRoundScore 69 ;
            clo-go:hasRunningScoreTotal 137 ;
            clo-go:isRoundNumber 2 ;
            clo-go:isRoundSubject <https://clojos.io/ontology/FantasyGolf/Ind/Tournament/ClojosOpen/2023/Leaderboard/Round/2> ]
        :param bn_sub:
        :return:
        """
        triples = rdf.all_matching(self.graph, (bn_sub, None, None))
        rd_num = rdf.triple_finder(rdf.isRoundNumber, triples)
        pos = rdf.triple_finder(rdf.hasPositionAfterRound, triples)
        score = rdf.triple_finder(rdf.hasRoundScore, triples)
        running_total = rdf.triple_finder(rdf.hasRunningScoreTotal, triples)
        rd_sub = rdf.triple_finder(rdf.isRoundSubject, triples)
        state = rdf.triple_finder(rdf.playerIsInState, triples)
        return RoundScore(rd_num.toPython(),
                          score.toPython(),
                          pos.toPython(),
                          running_total.toPython(),
                          state.toPython() if state else None,
                          rd_sub)

    def create_round_bnode(self, g, sub, round_sub, score_for_round):
        # if score_for_round['state']:
        #     breakpoint()
        bn = BNode()
        g.add((bn, rdf.isRoundSubject, round_sub))
        g.add((bn, rdf.isRoundNumber, Literal(score_for_round['round_number'])))
        g.add((bn, rdf.hasRoundScore, Literal(score_for_round['score'])))
        if (pos := score_for_round['current_pos']):
            g.add((bn, rdf.hasPositionAfterRound, Literal(pos)))

        if (state:=score_for_round['state']):
            g.add((bn, rdf.playerIsInState, Literal(score_for_round['state'].value)))
        g.add((bn, rdf.hasRunningScoreTotal, Literal(score_for_round['running_total'])))
        g.add((sub, rdf.hasRoundScores, bn))

    def update_round_position(self, score: model.PlayerScore, rd_sub: URIRef, position: int):
        self.graph.set((score.subject, rdf.isInCurrentPosition, Literal(score.current_position)))
        this_rd_bnode = self.find_bn_for_round(score.subject, rd_sub)
        self.graph.set((this_rd_bnode, rdf.hasPositionAfterRound, Literal(position)))

    def find_bn_for_round(self, score_sub, rd_sub):
        return self.find_fn_for_rd_sub(rd_sub, rdf.all_matching(self.graph, (score_sub, rdf.hasRoundScores, None),
                                                                form=rdf.object))

    def find_fn_for_rd_sub(self, rd_sub, bnodes: BNode):
        bn = fn.remove_none(
            [rdf.first_match(self.graph, (bn, rdf.isRoundSubject, rd_sub), form=rdf.subject) for bn in bnodes])
        if not bn or len(bn) > 1:
            breakpoint()
        return bn[0]
