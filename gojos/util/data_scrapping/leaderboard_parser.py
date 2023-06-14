from typing import Tuple, Dict
from functools import reduce, partial

from .event_web_parser import leaderboard_parser


def build_leaderboard(entries_file=None, players_file=None):
    (_format_entries(
        _format_players(_parser_for_event().build_leaderboard(), players_file),
        entries_file)
    )


def _parser_for_event():
    return leaderboard_parser


def _format_entries(entries, entries_file):
    if not entries_file:
        return entries
    py = reduce(_entry_def, entries, _entry_function())
    _write_file(entries_file, py)
    return entries


def _format_players(entries, players_file):
    if not players_file:
        return entries
    py = reduce(partial(_player_def, []), entries, _players_imports_hdr())
    _write_file(players_file, py)
    return entries


def _players_imports_hdr():
    return """from typing import Tuple, List, Optional
from gojos.model.player import Player
from gojos.players import players
"""


def _entry_def(py, entry):
    return py + entry.player_definition() + ",\n"


def _player_def(entries, py, entry):
    return py + _player_def_intialisation(entries, entry)


def _entry_function():
    return """from gojos.players import mens_players
def entries():
    return [
"""


def _player_def_intialisation(players_klass_names, player):
    klass_name = _format_klass_name(player.name)
    if players_klass_names.count(klass_name) > 0:
        klass_name = _deal_with_dup(klass_name, player.name)
    players_klass_names.append(klass_name)
    return f"{klass_name} = Player(\"{player.name}\", klass_name=\"{klass_name}\")\n\n"


def _format_klass_name(name):
    nm = name.rstrip().split(' ')[-1].replace("-", "_").replace("'", "")
    if nm[-1] in ['.']:
        return nm[0:-1]
    return nm


def _deal_with_dup(klass_name, name):
    first_name = name.split(' ')[0].replace("-", "_").replace("'", "").replace(".", "_")
    if first_name[-1] in "_":
        first_name = first_name[0:-1]
    return f"{klass_name}_{first_name}"


def _write_file(file_name, klasses):
    with open(f"{file_name}", 'w') as f:
        f.write(klasses)
