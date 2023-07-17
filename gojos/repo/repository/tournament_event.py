from typing import Tuple
from functools import partial
from itertools import groupby

from rdflib import Graph, URIRef, Literal, RDF

from gojos import rdf

from . import graphrepo


class TournamentEventRepo(graphrepo.GraphRepo):
    rdf_type = rdf.TOURNAMENT_EVENT

    def __init__(self, graph: Graph):
        self.graph = graph

    def upsert(self, event):
        rdf.subject_finder_creator(self.graph, event.subject, self.rdf_type, partial(self.creator, event))
        pass

    def creator(self, event, g, sub):
        g.add((sub, RDF.type, rdf.TOURNAMENT_EVENT))
        g.add((sub, rdf.skos.notation, Literal(event.name)))
        g.add((sub, rdf.isInYear, Literal(event.scheduled_in_year)))
        g.add((sub, rdf.isEventOf, event.is_event_of.subject))
        g.add((sub, rdf.hasFantasyPointsStrategy, event.points_strategy.subject()))
        g.add((sub, rdf.hasCutStrategy, event.cut_strategy.subject()))
        return g

    def get_all(self):
        return [self.to_event(event) for event in (rdf.many(rdf.query(self.graph, self._sparql())))]


    def find_by_year(self, tournament_sub, year):
        return self.to_event(rdf.single_result_or_none(rdf.query(self.graph,
                                                                   self._sparql(year=year,
                                                                                tournament_sub=tournament_sub))))
    def add_player_as_entry(self, event, player):
        self.graph.add((event.subject, rdf.hasEnteredPlayer, player.subject))
        pass

    def find_by_tournament(self, tournament_sub):
        events = rdf.many(rdf.query(self.graph, self._sparql(tournament_sub=tournament_sub)))
        return [self.to_event(event) for event in events]

    def get_by_sub(self, sub):
        return self.to_event(rdf.single_result_or_none(rdf.query(self.graph, self._sparql(sub=sub))))

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
