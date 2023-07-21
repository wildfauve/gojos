from typing import Tuple
from functools import partial
from itertools import groupby

from rdflib import Graph, URIRef, Literal, RDF

from gojos import rdf
from gojos.util import logger

from . import graphrepo


class LeaderBoardRepo(graphrepo.GraphRepo):
    rdf_type = rdf.LEADERBOARD

    def __init__(self, graph: Graph):
        self.graph = graph

    def upsert(self, event):
        rdf.subject_finder_creator(self.graph, event.subject, self.rdf_type, partial(self.creator, event))
        pass

    def creator(self, leaderboard, g, sub):
        g.add((sub, RDF.type, rdf.LEADERBOARD))
        g.add((sub, rdf.isForEvent, leaderboard.event.subject))
        return g

    def add_round(self, leaderboard, for_round):
        self.graph.add((leaderboard.subject, rdf.hasRound, for_round.subject))


    def add_scoring_player(self, leaderboard, player_score_sub: URIRef):
        self.graph.add((leaderboard.subject, rdf.isPlayerOnLeaderboard, player_score_sub))

    @logger.with_perf_log(name="Leaderboard.get_all")
    def get_all(self):
        return [self.to_event(event) for event in (rdf.many(rdf.query(self.graph, self._sparql())))]


    def find_by_year(self, tournament_sub, year):
        return self.to_event(rdf.single_result_or_none(rdf.query(self.graph,
                                                                   self._sparql(year=year,
                                                                                tournament_sub=tournament_sub))))
    def get_by_event_sub(self, event_sub):
        sub, _, _ = rdf.first_match(self.graph, (None, rdf.isForEvent, event_sub))
        return sub

    def get_entries(self, sub):
        return [player_sub for _, _, player_sub in  rdf.all_matching(self.graph, (sub, rdf.hasEnteredPlayer, None))]

    def to_event(self, result) -> Tuple:
        if not result:
            return None
        return (result.year.toPython(),
                result.event_name.toPython(),
                result.event,
                result.cut_strat,
                result.fant_strat,
                result.tournament_sub)

    # def _sparql(self, tournament_sub=None, year=None, sub=None):
    #     if not year and not tournament_sub and not sub:
    #         filter_criteria = None
    #     elif tournament_sub and year:
    #         filter_criteria = f"?tournament_sub = {tournament_sub.n3()} && ?year = {Literal(year).n3()}"
    #     elif tournament_sub and not year:
    #         filter_criteria = f"?tournament_sub = {tournament_sub.n3()}"
    #     else:
    #         filter_criteria = f"?event = {sub.n3()}"
    #
    #     filter = "" if not filter_criteria else f"filter({filter_criteria})"
    #
    #     return f"""
    #     select ?event ?event_name ?year ?cut_strat ?fant_strat ?tournament_sub
    #
    #     where {{
    #
  	#     ?event a clo-go:TournamentEvent ;
	#            skos:notation ?event_name ;
	#            clo-go:isInYear ?year ;
	#            clo-go:hasCutStrategy ?cut_strat ;
	#            clo-go:hasFantasyPointsStrategy ?fant_strat ;
    #            clo-go:isEventOf ?tournament_sub .
    #
    #     {filter} }}
    #     """
