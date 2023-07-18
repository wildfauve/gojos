from typing import Callable, List, Tuple
from rdflib import Graph
from pathlib import Path

from gojos import rdf, model
from gojos.util import singleton

DB_PLAYERS_LOCATION = (Path(__file__).parent.parent.parent / "data" / "db" / "players.ttl")
DB_FANTASY_LOCATION = (Path(__file__).parent.parent.parent / "data" / "db" / "fantasy.ttl")
DB_TOURNAMENT_LOCATION = (Path(__file__).parent.parent.parent / "data" / "db" / "tournament.ttl")


class Db:

    def __init__(self,
                 empty_graph_fn: Callable,
                 ttl_writer: Callable):
        self.tournament_graph = None
        self.players_graph = None
        self.fantasy_graph = None
        self.tournament_graph = None
        self.in_memory = None
        self.init_empty_graph_fn = empty_graph_fn
        self.ttl_writer = ttl_writer

    def drop(self):
        self.players_graph = None
        self.tournament_graph = None
        self.fantasy_graph = None
        [self.drop_graph(location) for location in self.graph_locations()]
        return self

    def graph_locations(self):
        return ['fantasy', 'players', 'tournament']

    def load(self):
        [self.load_graph(location) for location in self.graph_locations()]
        return self

    def drop_graph(self, loc_name: str):
        loc_path = self.location_name_to_location(loc_name)
        if loc_path.exists():
            self.ttl_writer(self.init_empty_graph_fn(), file=loc_path)
        return self


    def load_graph(self, loc_name: str):
        loc_path = self.location_name_to_location(loc_name)
        if loc_path.exists():
            setattr(self, f"{loc_name}_graph", self.init_empty_graph_fn().parse(loc_path))
        return self

    def location_name_to_location(self, name) -> Path:
        return getattr(RepoContext(), f"{name}_triples_location")

    def save(self, graph_names: List = None):
        save_args = self.persist_location_args(graph_names)
        for g, loc in save_args:
            self.ttl_writer(g, file=loc)
        return self

    def persist_location_args(self, locations=None):
        if not locations:
            breakpoint()
            # return [(self.tournament_graph, RepoContext().triples_location)]
        return [(getattr(self, f"{loc}_graph"), self.location_name_to_location(loc)) for loc in locations]

    def init_empty_graph(self) -> Graph:
        return self.init_empty_graph_fn()


class RepoContext(singleton.Singleton):

    def configure(self,
                  players_triples_location: Path = DB_PLAYERS_LOCATION,
                  fantasy_triples_location: Path = DB_FANTASY_LOCATION,
                  tournament_triples_location: Path = DB_TOURNAMENT_LOCATION) -> None:
        if not self.already_configured():
            self.players_triples_location = players_triples_location
            self.fantasy_triples_location = fantasy_triples_location
            self.tournament_triples_location = tournament_triples_location
        pass

    def already_configured(self):
        return (hasattr(self, 'players_triples_location') and
                hasattr(self, 'fantasy_triples_location') and
                hasattr(self, 'tournament_triples_location'))

    def db_ctx(self, db: Db):
        self.db = db


def empty_graph():
    return initgraph()


def init():
    return RepoContext().db_ctx(Db(empty_graph_fn=initgraph,
                                   ttl_writer=write_to_ttl).load())


def players_graph():
    return RepoContext().db.players_graph


def fantasy_graph():
    return RepoContext().db.fantasy_graph


def tournament_graph():
    return RepoContext().db.tournament_graph


def save(graph_names: List = None):
    return RepoContext().db.save(graph_names)


def reload():
    return init()


def drop():
    RepoContext().db.drop()


def initgraph() -> Graph:
    return rdf.bind(rdf_graph())


def rdf_graph():
    return Graph()


def write_to_ttl(g, format="turtle", file=None):
    if format == "turtle":
        txt = g.serialize(format=format)
    else:
        txt = g.serialize(format="json-ld", indent=4)
    if file:
        with open(file, 'w') as f:
            f.write(txt)
