from typing import Tuple, Dict
from functools import reduce, partial

from .event_web_parser import usopen_leaderboard_parser

lb_preamble = "tournie.leaderboard.for_round"

def build_leaderboard(for_round, entries_file=None, players_file=None, leaderboard_file=None):
    _format_leaderboard(
        _format_entries(
            _format_players(_parser_for_event().build_leaderboard(for_round), players_file),
            entries_file),
        leaderboard_file, for_round)


def _parser_for_event():
    return usopen_leaderboard_parser


def _format_leaderboard(entries, leaderboard_file, for_round):
    if not leaderboard_file:
        return entries
    py = _results_function()
    for rd, entries in reduce(partial(_leaderboard_def, for_round), entries, {1: [], 2: [], 3: [], 4: []}).items():
        if entries:
            py = py + f"\n\ndef scores(tournie):\n"
            for entry in entries:
                py = py + f"{'':>4}{entry}\n"
            py = py + f"{'':>4}tournie.leaderboard.for_round({rd}).done()\n"

    _write_file(leaderboard_file, py)
    return entries


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


def _results_function():
    return f"""from gojos.players.mens_players import *
from gojos.model.tournament_event import PlayerState

"""


def _leaderboard_def(for_round, accum, entry):
    return reduce(partial(_player_rd_score,entry), enumerate(entry.round_scores, start=for_round), accum)


def _player_rd_score(entry, accum, round_score):
    rd, score = round_score
    py = f"{lb_preamble}({rd}).player({entry.player_klass.klass_name}).score({score}).position({entry.current_position()})"
    accum[rd].append(py)
    return accum


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
