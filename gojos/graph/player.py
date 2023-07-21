from typing import Dict, Tuple
from dataclasses import dataclass

from rdflib import Graph, URIRef, Literal

from gojos import rdf

@dataclass
class P:
    sub: URIRef
    name: str
    klass_name: str

    def __hash__(self):
        return hash((self.sub,))

    def __eq__(self, other):
        if not self or not other:
            breakpoint()
        return self.sub == other.sub


def player_for(g: Graph, players: Dict, klass_name) -> Tuple[P, Dict]:
    if klass_name in players.keys():
        return players.get(klass_name), players

    sub = rdf.first_match(g, (None, rdf.hasKlassName, Literal(klass_name)), form=rdf.subject)
    triples = rdf.all_matching(g, (sub, None, None))
    plr = P(sub, rdf.triple_finder(rdf.name, triples), rdf.triple_finder(rdf.hasKlassName, triples))
    players.get('players').add(plr)
    return plr, {**players, **{klass_name: plr}}

def player_sub_by_name(g: Graph, name: str):
    return rdf.first_match(g, (None, rdf.name, Literal(name)), form=rdf.subject)