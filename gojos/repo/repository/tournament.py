from functools import partial
from itertools import groupby

from rdflib import Graph, URIRef, Literal, RDF

from . import graphrepo
from gojos.util import logger

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

    @logger.with_perf_log(name="Tournament.get_all")
    def get_all(self):
        return [self.to_tournie(sub) for sub in rdf.all_matching(self.graph, (None, RDF.type,rdf.TOURNAMENT), form=rdf.subject)]

    def get_by_sub(self, sub):
        return self.to_tournie(sub)

    def find_by_name(self, name):
        return self.to_tournie(rdf.first_match(self.graph, (None, rdf.skos.notation, Literal(name)), form=rdf.subject))

    def to_tournie(self, sub):
        if not sub:
            return None
        triples = rdf.all_matching(self.graph, (sub, None, None))
        name = rdf.triple_finder(rdf.skos.notation, triples)
        permid = rdf.triple_finder(rdf.hasPermId, triples)
        subject_name = rdf.triple_finder(rdf.hasSubjectName, triples)
        return (name.toPython(),
                subject_name.toPython(),
                permid.toPython(),
                sub)

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
