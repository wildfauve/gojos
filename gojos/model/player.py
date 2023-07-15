from typing import List
from functools import partial
from rdflib import Graph, URIRef, Literal, RDF
from gojos.util import fn, tokeniser

from gojos import model


class Player:

    @classmethod
    def player_predicate(cls, test_for_player, player):
        return test_for_player == player

    @classmethod
    def format_player_klass_name(cls, name):
        nm = name.rstrip().lstrip()
        if "." in nm:
            return tokeniser.string_tokeniser(nm, tokeniser.dot_splitter, tokeniser.special_char_set)
        return tokeniser.string_tokeniser(nm, tokeniser.sp_splitter, tokeniser.special_char_set)


    def __init__(self, name, klass_name: str, alt_names: List = None):
        self.name = name
        self.klass_name = klass_name
        self.alt_names = alt_names if alt_names else []

    def __repr__(self):
        return f"Player(klass={self.klass_name}, name={self.name})"

    def uri_name(self):
        return self.name.split(" ")[-1]

    def __hash__(self):
        return hash((self.name,))

    def __eq__(self, other):
        if not self or not other:
            breakpoint()
        return self.name == other.name

    def match_by_name(self, on_name):
        if self.__class__.format_player_klass_name(on_name) == self.klass_name:
            return self
        if self.name == on_name:
            return self
        if self.__class__.format_player_klass_name(on_name) in self.klass_name:
            if any([alt_name == on_name for alt_name in self.alt_names]):
                return self
        return None


class PlayerScore:

    player_score_cache = []

    @classmethod
    def scoring_for_player(cls, player, round_number):
        from_cache = cls.player_from_cache(player)
        if not from_cache:
            ps = cls(player, round_number)
            cls.player_score_cache.append(ps)
            return ps
        from_cache.current_round = round_number
        return from_cache

    @classmethod
    def player_from_cache(cls, player):
        if not cls.player_score_cache:
            return None
        return fn.find(partial(cls._player_predicate, player), cls.player_score_cache)

    @classmethod
    def _player_predicate(cls, test_for_player, player_score):
        return test_for_player == player_score.player


    def __init__(self, player, current_round):
        self.player = player
        self.current_round = current_round
        self.rounds = {1: None, 2: None, 3: None, 4: None}
        self.overall_total = None
        self.round_score = None
        self.current_position = None
        self.player_state = None
        self.total = 0

    def score(self, scr):
        if not scr:
            self.rounds[self.current_round] = {'score': scr, 'current_pos': None}
            return self
        self.rounds[self.current_round] = {'score': scr, 'current_pos': None, 'running_total': self.total + scr}
        self.total += scr
        self.round_score = scr
        return self

    def position(self, pos, rd_number: int = None):
        if isinstance(pos, model.PlayerState):
            self.player_state = pos
        self.current_position = pos
        if rd_number:
            self.rounds[rd_number]['current_pos'] = pos
        return self

