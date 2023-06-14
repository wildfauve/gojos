from functools import partial

from gojos import model
from gojos.util import fn

from . import mens_players

player_cache = {'mens_players': []}


def match_player_by_name(name, player_module):
    print(f"finding...{name}")
    result = list(fn.select(partial(_player_finder, name), _player_cache(player_module)))
    if len(result) == 1:
        return result[0]
    if not result:
        return None
    breakpoint()


def _player_finder(name, player):
    return player.match_by_name(name)


def format_player_klass_name(self):
    return fn.multi_replace(self.name.rstrip().split(name_split_char)[-1], klass_name_replace_set)


def _player_cache(player_module):
    if player_cache[_cache(player_module)]:
        return player_cache[_cache(player_module)]
    attrs = [getattr(player_module, attr) for attr in dir(player_module) if "__" not in attr]
    player_cache[_cache(player_module)] = [attr for attr in attrs if isinstance(attr, model.Player)]
    return player_cache[_cache(player_module)]


def _cache(player_module):
    return player_module.__name__.split(".")[-1]
