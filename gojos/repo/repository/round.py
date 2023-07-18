from __future__ import annotations
from typing import Tuple
from functools import partial
from itertools import groupby

from rdflib import Graph, URIRef, Literal, RDF

from gojos import rdf, model

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
        return [self.build_round(sub) for sub in rdf.all_matching(self.graph, (None, rdf.isRoundOnLeaderboard, lb_sub), form=rdf.subject)]


    def build_round(self, rd_sub):
        rd_triples = rdf.all_matching(self.graph, (rd_sub, None, None))
        rd_number = rdf.triple_finder(rdf.isRoundNumber, rd_triples)
        return (rd_sub, rd_number.toPython())


    def find_by_year(self, tournament_sub, year):
        return self.to_event(rdf.single_result_or_none(rdf.query(self.graph,
                                                                 self._sparql(year=year,
                                                                              tournament_sub=tournament_sub))))

    def get_by_event_sub(self, event_sub):
        sub, _, _ = rdf.first_match(self.graph, (event_sub, rdf.hasLeaderboard, None))
        if not sub:
            return None
        breakpoint()
        return self.to_event(rdf.single_result_or_none(rdf.query(self.graph, self._sparql(sub=sub))))

    def get_entries(self, sub):
        return [player_sub for _, _, player_sub in rdf.all_matching(self.graph, (sub, rdf.hasEnteredPlayer, None))]

    def to_event(self, result) -> Tuple:
        if not result:
            return None
        return (result.year.toPython(),
                result.event_name.toPython(),
                result.event,
                result.cut_strat,
                result.fant_strat,
                result.tournament_sub)

    def _sparql(self, tournament_sub=None, year=None, sub=None):
        if not year and not tournament_sub and not sub:
            filter_criteria = None
        elif tournament_sub and year:
            filter_criteria = f"?tournament_sub = {tournament_sub.n3()} && ?year = {Literal(year).n3()}"
        elif tournament_sub and not year:
            filter_criteria = f"?tournament_sub = {tournament_sub.n3()}"
        else:
            filter_criteria = f"?event = {sub.n3()}"

        filter = "" if not filter_criteria else f"filter({filter_criteria})"

        return f"""
        select ?event ?event_name ?year ?cut_strat ?fant_strat ?tournament_sub

        where {{

  	    ?event a clo-go:TournamentEvent ;
	           skos:notation ?event_name ;
	           clo-go:isInYear ?year ;
	           clo-go:hasCutStrategy ?cut_strat ;
	           clo-go:hasFantasyPointsStrategy ?fant_strat ;
               clo-go:isEventOf ?tournament_sub .

        {filter} }}
        """
