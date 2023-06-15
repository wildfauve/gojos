from typing import Callable, List
from dataclasses import dataclass

import bs4

from gojos.players import players
from gojos.util import fn


@dataclass
class ScrappedPlayer:
    name: str
    player_module: Callable
    round_scores: List[int] = None
    position: int = None
    total: int = None

    def __post_init__(self):
        self.player_klass = players.match_player_by_name(self.name, self.player_module)
        if not self.player_klass:
            breakpoint()


    def player_entry_klass_name(self):
        return self.player_klass.klass_name

    def entry_definition(self):
        return f"{'':>12}({self.player_definition()}, {self._seed()}),\n"

    def player_definition(self):
        return f"{self._player_mod_name()}.{self.player_entry_klass_name()}"

    def _player_mod_name(self):
        return self.player_module.__name__.split(".")[-1]
