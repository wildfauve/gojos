from __future__ import annotations
from typing import Tuple
from functools import partial
from itertools import groupby

from rdflib import Graph, URIRef, Literal, RDF

from gojos import rdf, model
from gojos.util import logger

from . import graphrepo


class RoundRepo(graphrepo.GraphRepo):
    rdf_type = rdf.ROUND

    def __init__(self, graph: Graph):
        self.graph = graph

    def upsert(self, event):
        rdf.subject_finder_creator(self.graph, event.subject, self.rdf_type, partial(self.creator, event))
        pass

    def creator(self, for_round: model.Round, g, sub):
        g.add((sub, RDF.type, rdf.ROUND))
        g.add((sub, rdf.isRoundNumber, Literal(for_round.round_number)))
        g.add((sub, rdf.isRoundOnLeaderboard, for_round.leaderboard.subject))
        return g

    def get_all(self, lb_sub):
        return self.get_build_all(lb_sub, perf_ctx=lb_sub)

    @logger.with_perf_log(name="Round.get_build_all")
    def get_build_all(self, lb_sub, perf_ctx):
        return [self.build_round(sub) for sub in
                rdf.all_matching(self.graph, (None, rdf.isRoundOnLeaderboard, lb_sub), form=rdf.subject)]

    def build_round(self, rd_sub):
        rd_triples = rdf.all_matching(self.graph, (rd_sub, None, None))
        rd_number = rdf.triple_finder(rdf.isRoundNumber, rd_triples)
        return (rd_sub, rd_number.toPython())

    def get_entries(self, sub):
        return [player_sub for _, _, player_sub in rdf.all_matching(self.graph, (sub, rdf.hasEnteredPlayer, None))]
