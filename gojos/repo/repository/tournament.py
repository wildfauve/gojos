from functools import partial
from itertools import groupby

from rdflib import Graph, URIRef, Literal, RDF

from . import graphrepo

from gojos import rdf


class TournamentRepo(graphrepo.GraphRepo):
    rdf_type = rdf.TOURNAMENT

    def __init__(self, graph: Graph):
        self.graph = graph

    def upsert(self, tournament):
        rdf.subject_finder_creator(self.graph, tournament.subject, self.rdf_type, partial(self.creator, tournament))
        pass

    def creator(self, tournament, g, sub):
        g.add((sub, RDF.type, rdf.TOURNAMENT))
        g.add((sub, rdf.skos.notation, Literal(tournament.name)))
        g.add((sub, rdf.hasPermId, Literal(tournament.perma_id)))
        g.add((sub, rdf.hasSubjectName, Literal(tournament.subject_name)))
        return g

    def get_all(self):
        return [self.to_tournie(tournie) for tournie in (rdf.many(rdf.query(self.graph, self._sparql())))]

    def get_by_sub(self, sub):
        return self.to_tournie(rdf.single_result_or_none(rdf.query(self.graph, self._sparql(sub=sub))))

    def find_by_name(self, name):
        return self.to_tournie(rdf.single_result_or_none(rdf.query(self.graph, self._sparql(name=name))))

    def to_tournie(self, result):
        if not result:
            return None
        return (result.tournie_name.toPython(),
                result.sub_name.toPython(),
                result.permid.toPython(),
                result.sub)

    def _sparql(self, name=None, sub=None):
        if not name and not sub:
            filter_criteria = None
        elif name:
            filter_criteria = f"?tournie_name = {Literal(name).n3()}"
        else:
            filter_criteria = f"?sub = {sub.n3()}"
        filter = "" if not filter_criteria else f"filter({filter_criteria})"

        return f"""
        select ?sub ?tournie_name ?permid ?sub_name

        where {{
  
        ?sub a clo-go:Tournament ;
                 clo-go:hasPermId ?permid ;
                 clo-go:hasSubjectName ?sub_name ;
  	             skos:notation ?tournie_name .

        {filter} }}
        """
