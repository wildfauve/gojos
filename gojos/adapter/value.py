from __future__ import annotations
from typing import Callable, List, Dict
from dataclasses import dataclass

from gojos import model
from gojos.util import logger

missing_file_name = '_temp/missing.py'

@dataclass
class ScrappedPlayer:
    name: str
    player_module: Callable
    round_scores: Dict = None
    position: int = None
    player_state: model.PlayerState = None
    total: int = None

    def __post_init__(self):
        self.player_klass = model.Player.load(name=self.name)
        if not self.player_klass:
            with open('_temp/missing.py', 'a') as missing_file:
                possible_klass_name = model.Player.format_player_klass_name(self.name)
                if (found_player := model.Player.load(klass_name=possible_klass_name)):
                    breakpoint()
                plyr_def = (f"{possible_klass_name} = model.Player.new('{self.name}',klass_name='{possible_klass_name}')\n")
                logger.debug(f"Cant find player: {plyr_def}")
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
