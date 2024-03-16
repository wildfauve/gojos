from functools import partial
from itertools import groupby

from rdflib import Graph, URIRef, Literal, RDF

from gojos import rdf
from gojos.util import logger
from . import graphrepo


class PlayerRepo(graphrepo.GraphRepo):
    rdf_type = rdf.PLAYER

    def __init__(self, graph: Graph):
        self.graph = graph

    @logger.with_perf_log(name="Player.get_all")
    def get_all(self):
        return [self.to_player(sub) for sub in rdf.all_matching(self.graph, (None, RDF.type, rdf.PLAYER), form=rdf.subject)]


    def to_player(self, sub):
        if not sub:
            return None
        triples = rdf.all_matching(self.graph, (sub, None, None))
        name = rdf.triple_finder(rdf.name, triples)
        klass_name = rdf.triple_finder(rdf.hasKlassName, triples)
        if not name:
            breakpoint()
        return (sub,
                name.toPython(),
                klass_name.toPython(),
                None)  # no alt names

    def upsert(self, player):
        rdf.subject_finder_creator(self.graph, player.subject, self.rdf_type, partial(self.creator, player))
        pass

    def get_by_name_or_klass_name(self, sub=None, name=None, klass_name=None, alt_name=None):
        if sub:
            return self.to_player(sub)
        if name:
            return self.to_player(rdf.first_match(self.graph, (None, rdf.name, Literal(name)), form=rdf.subject))
        if klass_name:
            return self.to_player(rdf.first_match(self.graph, (None, rdf.hasKlassName, Literal(name)), form=rdf.subject))
        breakpoint()

    def creator(self, player, g, sub):
        g.add((sub, RDF.type, self.rdf_type))
        g.add((sub, rdf.name, Literal(player.name)))
        g.add((sub, rdf.hasKlassName, Literal(player.klass_name)))
        for alt in player.alt_names:
            g.add((sub, rdf.hasAlternateName, Literal(alt)))
