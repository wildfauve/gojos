from __future__ import annotations
from typing import Tuple
from functools import partial
from itertools import groupby

from rdflib import Graph, URIRef, Literal, RDF, BNode

from gojos import rdf, model
from gojos.util import fn

from . import graphrepo


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
        self.create_round_bnode(self.graph, score.subject, rd_sub, score.rounds[rd_sub])
        self.graph.set((score.subject, rdf.hasScoreTotal, Literal(score.total)))

    def create_round_bnode(self, g, sub, round_sub, score_for_round):
        bn = BNode()
        g.add((bn, rdf.isRoundSubject, round_sub))
        g.add((bn, rdf.isRoundNumber, Literal(score_for_round['round_number'])))
        g.add((bn, rdf.hasRoundScore, Literal(score_for_round['score'])))
        if (pos := score_for_round['current_pos']):
            g.add((bn, rdf.hasPositionAfterRound, Literal(pos)))
        g.add((bn, rdf.hasRunningScoreTotal, Literal(score_for_round['running_total'])))
        g.add((sub, rdf.hasRoundScores, bn))

    def update_round_position(self, score: model.PlayerScore, rd_sub: URIRef, position: int):
        self.graph.set((score.subject, rdf.isInCurrentPosition, Literal(score.current_position)))
        this_rd_bnode = self.find_bn_for_round(score.subject, rd_sub)
        self.graph.set((this_rd_bnode, rdf.hasPositionAfterRound, Literal(position)))

    def find_bn_for_round(self, score_sub, rd_sub):
        return self.find_fn_for_rd_sub(rd_sub, rdf.all_matching(self.graph, (score_sub, rdf.hasRoundScores, None), form=rdf.object))

    def find_fn_for_rd_sub(self, rd_sub, bnodes: BNode):
        bn = fn.remove_none([rdf.first_match(self.graph, (bn, rdf.isRoundSubject, rd_sub), form=rdf.subject) for bn in bnodes])
        if not bn or len(bn) > 1:
            breakpoint()
        return bn[0]