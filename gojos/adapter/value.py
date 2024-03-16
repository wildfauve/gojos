from __future__ import annotations
from typing import Callable, List, Dict
from dataclasses import dataclass

from gojos import model
from gojos.util import logger

missing_file_name = '_temp/missing.py'
missing_rdf_file_name = '_temp/missing.ttl'

@dataclass
class ScrappedPlayer:
    name: str
    player_module: Callable
    round_scores: Dict = None
    position: int = None
    player_state: model.PlayerState = None
    total: int = None
    missing_writer: Callable = None

    def __post_init__(self):
        logger.debug(f"Scaping Player: {self.name}, scores: {self.round_scores}")
        self.player_klass = model.Player.load(name=self.name)
        if not self.player_klass:
            possible_klass_name = model.Player.format_player_klass_name(self.name)
            if (found_player := model.Player.load(klass_name=possible_klass_name)):
                breakpoint()
            plyr_def = self.python_player_def(possible_klass_name)
            rdf_def = self.rdf_player_def(possible_klass_name)
            logger.debug(f"Cant find player: {plyr_def}\n\n{rdf_def}")
            if not self.missing_writer:
                self.missing_file_writer(plyr_def, rdf_def)
            else:
                self.missing_writer(plyr_def)

    def rdf_player_def(self, possible_klass_name):
        return f'''clo-go-ind-plr:{possible_klass_name} a clo-go:Player ;
foaf:name "{self.name}" ;
clo-go-plr:hasKlassName "{possible_klass_name}" .
\n\n'''


    def python_player_def(self, possible_klass_name):
        return f"{possible_klass_name} = model.Player.new('{self.name}',klass_name='{possible_klass_name}')\n"

    def missing_file_writer(self, plyr_def, rdf_def):
        with open(missing_file_name, 'a') as missing_file:
            missing_file.write(plyr_def)
        with open(missing_rdf_file_name, 'a') as missing_file:
            missing_file.write(rdf_def)


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
