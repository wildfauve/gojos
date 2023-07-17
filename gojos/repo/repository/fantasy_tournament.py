from functools import partial
from itertools import groupby

from rdflib import Graph, URIRef, Literal, RDF

from . import graphrepo

from gojos import rdf
from gojos.util import fn


class FantasyTournamentRepo(graphrepo.GraphRepo):
    rdf_type = rdf.FANTASY_TOURNAMENT

    def __init__(self, graph: Graph):
        self.graph = graph

    def upsert(self, team):
        rdf.subject_finder_creator(self.graph, team.subject, self.rdf_type, partial(self.creator, team))
        pass

    def creator(self, fantasy, g, sub):
        g.add((sub, RDF.type, rdf.FANTASY_TOURNAMENT))
        g.add((sub, rdf.isForTeam, fantasy.team.subject))
        g.add((sub, rdf.isFantasyForEvent, fantasy.event.subject))
        return g

    def get_all(self):
        return [self.to_team(team) for team in (rdf.many(rdf.query(self.graph, self._sparql())))]

    def get_by_sub(self, sub):
        return self.to_tournie(rdf.single_result_or_none(rdf.query(self.graph, self._sparql(sub=sub))))

    def find_by_name(self, name):
        return self.to_team(rdf.single_result_or_none(rdf.query(self.graph, self._sparql(name=name))))

    def to_team(self, team):
        if not team:
            return None
        sub, name = team
        team_triples = rdf.all_matching(self.graph, (sub, None, None))
        members = rdf.triple_finder(rdf.hasTeamMembers, team_triples)
        features = rdf.triple_finder(rdf.hasFeature, team_triples, filter_fn=fn.select, builder=rdf.all_objects)
        return (name.toPython(),
                members.toPython(),
                [feat.toPython() for feat in features],
                sub)

    def _sparql(self, name=None, sub=None):
        if not name and not sub:
            filter_criteria = None
        elif name:
            filter_criteria = f"?team_name = {Literal(name).n3()}"
        else:
            filter_criteria = f"?sub = {sub.n3()}"
        filter = "" if not filter_criteria else f"filter({filter_criteria})"

        return f"""
        select ?sub ?team_name 

        where {{
  
        ?sub a clo-fan:Team ;
  	           skos:notation ?team_name .

        {filter} }}
        """
