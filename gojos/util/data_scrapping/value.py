from typing import Callable, List
from dataclasses import dataclass

import bs4

from gojos.players import players
from gojos.model import tournament_event, player
from gojos.util import fn

missing_file_name = '_temp/missing.py'

@dataclass
class ScrappedPlayer:
    name: str
    player_module: Callable
    round_scores: List[int] = None
    position: int = None
    player_state: tournament_event.PlayerState = None
    total: int = None

    def __post_init__(self):
        self.player_klass = players.match_player_by_name(self.name, self.player_module)
        if not self.player_klass:
            with open('_temp/missing.py', 'a') as missing_file:
                possible_klass_name = player.Player.format_player_klass_name(self.name)
                if players.player_by_klass_name(possible_klass_name, self.player_module):
                    breakpoint()
                plyr_def = (f"{possible_klass_name} = Player('{self.name}',klass_name='{possible_klass_name}')\n")
                print(f"Cant find player: {plyr_def}")
                missing_file.write(plyr_def)

    def player_entry_klass_name(self):
        return self.player_klass.klass_name

    def entry_definition(self):
        return f"{'':>12}({self.player_definition()}, {self._seed()}),\n"

    def player_definition(self):
        return f"{self._player_mod_name()}.{self.player_entry_klass_name()}"

    def current_position(self):
        return self.player_state if self.player_state else self.position

    def _player_mod_name(self):
        return self.player_module.__name__.split(".")[-1]
