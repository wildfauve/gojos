from typing import List
from functools import partial
from rdflib import Graph, URIRef, Literal, RDF
from gojos.util import fn, tokeniser


class Player:

    def __init__(self, name, klass_name: str, alt_names: List = None):
        self.name = name
        self.klass_name = klass_name
        self.alt_names = alt_names if alt_names else []

    def __repr__(self):
        return f"Player(klass={self.klass_name}, name={self.name})"

    def _format_player_klass_name(self, name):
        nm = name.rstrip().lstrip()
        if "." in nm:
            return tokeniser.string_tokeniser(nm, tokeniser.dot_splitter, tokeniser.special_char_set)
        return tokeniser.string_tokeniser(nm, tokeniser.sp_splitter, tokeniser.special_char_set)

    def uri_name(self):
        return self.name.split(" ")[-1]

    def __hash__(self):
        return hash((self.name,))

    def __eq__(self, other):
        if not self or not other:
            breakpoint()
        return self.name == other.name

    def match_by_name(self, on_name):
        if self._format_player_klass_name(on_name) == self.klass_name:
            return self
        if self.name == on_name:
            return self
        if self._format_player_klass_name(on_name) in self.klass_name:
            if any([alt_name == on_name for alt_name in self.alt_names]):
                return self
        return None
