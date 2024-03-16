from typing import Union, Tuple, Dict
import sys

from rdflib import URIRef

from . import player
from gojos import model, rdf
from gojos.repo import repository
from gojos.util import singleton, fn


class Tournament:
    repo = model.GraphModel(repository.TournamentRepo, model.GraphModel.tournament_graph)

    @classmethod
    def reset(cls):
        cls.repo = model.GraphModel(repository.TournamentRepo, model.GraphModel.tournament_graph)

    @classmethod
    def create(cls, name: str, subject_name: str, perma_id: str):
        tournie = cls(name, subject_name, perma_id)
        cls.repo().upsert(tournie)
        return tournie

    @classmethod
    def get_all(cls):
        return [cls(*tournie) for tournie in cls.repo().get_all()]

    @classmethod
    def get(cls, name):
        tournie = cls.repo().find_by_name(name)
        if not tournie:
            return None
        return cls(*tournie)

    @classmethod
    def get_by_sub(cls, sub: URIRef):
        tournie = cls.repo().get_by_sub(sub)
        if not tournie:
            return None
        return cls(*tournie)

    def __init__(self, name, subject_name: str, perma_id: str, sub: URIRef = None):
        self.name = name
        self.perma_id = perma_id
        self.subject_name = subject_name
        self.subject = rdf.clo_go_ind_tou[subject_name] if not sub else sub
        self.events = []

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name})"

    def __hash__(self):
        return hash((self.subject,))

    def __eq__(self, other):
        if not self or not other:
            return None
        return self.subject == other.subject

    def make_event(self, year, cut_strategy: str = None):
        event = fn.find(lambda ev: ev.scheduled_in_year == year, self.events)
        if event:
            return event
        event = model.TournamentEvent.create(year=year, tournament=self, cut_strategy=cut_strategy)
        self.events.append(event)
        return event

    def for_year(self, year, load: bool = False):
        event = fn.find(lambda event: event.scheduled_in_year == year, self.events)
        if not load:
            return event
        return event.load()

    def all_events(self):
        self.events = model.TournamentEvent.get_all_for_tournament(self)
        return self


class GrandSlam(Tournament):
    pass


class Course:
    def __init__(self, name, par, country_symbol):
        self.name = name
        self.par = par
        self.country_symbol = country_symbol


class Cut:

    @classmethod
    def build(cls, sub: Union[URIRef, str]):
        if isinstance(sub, URIRef):
            klass_name = sub.split("/")[-1]
        else:
            klass_name = sub
        klass = getattr(sys.modules[__name__], klass_name)
        return klass()

    def subject(self):
        return URIRef(
            rdf.CUT_STRATEGY) + f"/{self.__class__.__name__}"

    def below_cut_line(self, player_score: model.PlayerScore):
        return self.player_below_cut(player_score)

    def relative_to_cut(self, position):
        return self._position_from_cut(position)


class CutTop60AndTies(Cut):
    cut_position = 60

    def _position_from_cut(self, position):
        if isinstance(position, model.PlayerState) or not position:
            return -1
        if position == self.cut_position:
            return 0
        return self.cut_position - position


class CutTop65AndTies(Cut):
    cut_position = 65

    def _position_from_cut(self, rd_position: dict):
        if isinstance(rd_position, model.PlayerState) or not rd_position:
            return -1
        pos = rd_position.get('current_pos')
        if pos == self.cut_position:
            return 0
        return self.cut_position - pos


class CutTop70AndTies(Cut):
    cut_position = 70

    def _position_from_cut(self, rd_position: Dict):
        if isinstance(rd_position, model.PlayerState) or not rd_position:
            return -1
        pos = rd_position.get('current_pos')
        if pos == self.cut_position:
            return 0
        return self.cut_position - pos


class TournamentFinder(singleton.Singleton):

    def add_touraments(self, tournies):
        self.tournaments = tournies

    def slam(self, symbol):
        return fn.find(lambda tournie: tournie.subject_name == symbol, self.tournaments)

    def slam_names(self):
        return [tournie.name for tournie in self.tournaments]

    def slam_symbols(self):
        return [tournie.subject_name for tournie in self.tournaments]

    def slam_year(self, name, year, load: bool = False):
        tournie = self.slam(name)
        return tournie, tournie.for_year(year, load=load)


def tournaments():
    all_tournies = GrandSlam.get_all()
    TournamentFinder().add_touraments([Tournament.all_events(tournie) for tournie in all_tournies])
    return TournamentFinder()
