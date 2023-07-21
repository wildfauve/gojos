from typing import List, Tuple, Dict
from rdflib import Graph, URIRef, Literal, RDF

from gojos.rdf import rdf_prefix
from gojos.util import fn, tokeniser, monad, singleton, logger
from gojos import model, rdf
from gojos.repo import repository
from gojos.players import mens_players


class PlayerCache(singleton.Singleton):
    player_name_index = {}
    players = {}
    mens_players_module = mens_players

    def clear(self):
        self.__class__.player_name_index = {}
        self.__class__.players = {}
        return self

    def get_by_name_or_klass_or_sub(self, name=None, klass_name=None, sub=None):
        if name:
            possible_hit = self.__class__.player_name_index.get(name, None)
        elif klass_name:
            possible_hit = self.__class__.players.get(klass_name, None)
        else:
            possible_hit = fn.find(lambda plr: plr.subject == sub, self.__class__.players.values())
        if possible_hit and isinstance(possible_hit, str):
            return monad.Right(self.__class__.players[possible_hit])
        if not possible_hit:
            return monad.Left(None)
        return monad.Right(possible_hit)

    def add_to_cache(self, player):
        self.set_player_on_player_module(player)
        if self.get_by_name_or_klass_or_sub(klass_name=player.klass_name).is_right():
            return monad.Right(player)
        self.__class__.players[player.klass_name] = player
        self.__class__.player_name_index[player.name] = player.klass_name
        monad.Right(player)

    def set_player_on_player_module(self, player):
        setattr(self.__class__.mens_players_module, player.klass_name, player)
        pass



class Player:
    repo = model.GraphModel(repository.PlayerRepo, model.GraphModel.player_graph)
    player_cache = PlayerCache

    @classmethod
    def reset(cls):
        cls.repo = model.GraphModel(repository.PlayerRepo, model.GraphModel.player_graph)
        cls.player_cache = PlayerCache

    @classmethod
    def new(cls, name, klass_name: str, alt_names: List = None):
        cached_player = cls.cache_hit(name=name)
        if cached_player.is_right():
            return cached_player.value

        plr = cls.cls_search(name=name, alt_name=name)
        if plr.is_right():
            cls.build_player(plr.value)
        player = cls(name, klass_name, alt_names)
        cls.player_cache().add_to_cache(player)
        cls.repo().upsert(player)
        return player

    @classmethod
    def load(cls, name: str = None, klass_name: str = None, sub: URIRef = None):
        cached_player = cls.cache_hit(name=name, klass_name=klass_name, sub=sub)
        if cached_player.is_right():
            logger.log(f"Player Cache Hit: {cached_player.value}")
            return cached_player.value

        plr = cls.cls_search(sub=sub, name=name, klass_name=klass_name, alt_name=name)
        if plr.is_left():
            logger.log(f"Player with Name {name} or klass_name {klass_name} not found")
            return None
        player = cls.build_player(plr.value)
        cls.player_cache().add_to_cache(player)
        return player

    @classmethod
    def loadall(cls):
        for plr in cls.repo().get_all():
            player = cls.build_player(plr)
            cls.player_cache().add_to_cache(player)
        pass

    @classmethod
    def build_player(cls, player_tuple):
        sub, name, klass_name, alt_names = player_tuple
        return cls(name, klass_name, alt_names, sub)

    @classmethod
    def cls_search(cls, sub=None, name=None, klass_name=None, alt_name=None) -> monad.EitherMonad[Tuple]:
        plr = cls.repo().get_by_name_or_klass_name(sub=sub, name=name, klass_name=klass_name, alt_name=alt_name)
        if not plr:
            return monad.Left(plr)
        return monad.Right(plr)

    @classmethod
    def cache_hit(cls, name=None, klass_name=None, sub=None):
        return cls.player_cache().get_by_name_or_klass_or_sub(name=name, klass_name=klass_name, sub=sub)

    @classmethod
    def player_predicate(cls, test_for_player, player):
        return test_for_player == player

    @classmethod
    def format_player_klass_name(cls, name):
        nm = name.rstrip().lstrip()
        if "." in nm:
            return tokeniser.string_tokeniser(nm, tokeniser.dot_splitter, tokeniser.special_char_set)
        return tokeniser.string_tokeniser(nm, tokeniser.sp_splitter, tokeniser.special_char_set)

    def __init__(self, name, klass_name: str, alt_names: List = None, sub: URIRef = None):
        self.name = name
        self.klass_name = klass_name
        self.alt_names = alt_names if alt_names else []
        self.subject = rdf_prefix.clo_go_ind_plr[klass_name] if not sub else sub

    def __repr__(self):
        return f"Player(klass='{self.klass_name}', name='{self.name}')"

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
