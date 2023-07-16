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

    def get_all(self):
        results = rdf.many(rdf.query(self.graph, self._name_sparql()))
        return [self.to_player(player, props) for player, props in groupby(results, lambda x: x[0])]

    def to_player(self, player, props):
        player_props = props if isinstance(props, list) else list(props)
        return (player_props[0].sub,
                player_props[0].name.toPython(),
                player_props[0].klass_name.toPython(),
                [r.alt_names.toPython() for r in player_props] if player_props[0].alt_names else None)

    def upsert(self, player):
        rdf.subject_finder_creator(self.graph, player.subject, self.rdf_type, partial(self.creator, player))
        pass

    def get_by_name_or_klass_name(self, name=None, klass_name=None, alt_name=None):
        result = rdf.many(rdf.query(self.graph, self._name_sparql(name=name, klass_name=klass_name, alt_name=alt_name)))
        if not result:
            return None
        return self.to_player(result[0].sub, result)

    def creator(self, player, g, sub):
        g.add((sub, RDF.type, self.rdf_type))
        g.add((sub, rdf.name, Literal(player.name)))
        g.add((sub, rdf.hasKlassName, Literal(player.klass_name)))
        for alt in player.alt_names:
            g.add((sub, rdf.hasAlternateName, Literal(alt)))

    def _name_sparql(self, name=None, klass_name=None, alt_name=None):
        if not name and not klass_name and not alt_name:
            filter_criteria = None
        elif name:
            filter_criteria = f"?name = {Literal(name).n3()}"
        else:
            filter_criteria = f"?klass_name = {Literal(klass_name).n3()}"

        if alt_name:
            filter_criteria += f" || ?alt_names = {Literal(alt_name).n3()}"

        filter = "" if not filter_criteria else f"filter({filter_criteria})"
        logger.log(filter)

        return f"""
        select ?sub ?name ?klass_name ?alt_names

        where {{
        
        ?sub a clo-go:Player ;
             foaf:name ?name ;
             clo-go-plr:hasKlassName ?klass_name .
             
        OPTIONAL {{ ?sub clo-go-plr:hasAltName ?alt_names .}} 
    
        {filter} }}
        """
