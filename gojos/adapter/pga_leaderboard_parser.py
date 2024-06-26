from typing import Tuple, Union, Callable
from functools import reduce, partial
import json

from csvw import CSVW

import requests
from bs4 import BeautifulSoup

from gojos.players import mens_players
from gojos import model
from gojos.util import fn, logger

from . import value

leaderboard = "https://www.pgatour.com/leaderboard"
# leaderboard = "https://www.pgatour.com/tournaments/2024/masters-tournament/R2024014"


def build_leaderboard(for_round: int, to_model: bool = True, missing_player_writer: Callable = None):
    return _csvw_parser(_entries(_get_page(leaderboard)), for_round, to_model, missing_player_writer)


def _get_page(url_or_file):
    if 'http' in url_or_file:
        return BeautifulSoup(requests.get(url_or_file).text, "html.parser")
    return BeautifulSoup(open(url_or_file, encoding='UTF-8'), "html.parser")


def _entries(page):
    return page.find('script', type='application/ld+json').text


def _csvw_parser(json_ld, for_round, to_model, missing_player_writer):
    data = json.loads(json_ld)
    num_players = len(data['mainEntity']['csvw:tableSchema']['csvw:columns'][1]['csvw:cells'])
    return [_per_player_row(for_round,
                            data['mainEntity']['csvw:tableSchema']['csvw:columns'],
                            idx,
                            to_model,
                            missing_player_writer) for idx in range(0, num_players)]


def _per_player_row(for_round, table, cell_id, to_model, missing_player_writer):
    player_state = None
    pos = _to_int(_extract_value(table, 0, cell_id, "-"))
    name = _extract_value(table, 1, cell_id, "-")
    rds = {
        "this": _extract_value(table, for_round + 3, cell_id, "-"),
        1: _extract_value(table, 4, cell_id, "-"),
        2: _extract_value(table, 5, cell_id, "-"),
        3: _extract_value(table, 6, cell_id, "-"),
        4: _extract_value(table, 7, cell_id, "-")
    }
    if pos == "CUT":
        pos = None
        player_state = model.PlayerState.CUT
    if pos == "WD":
        pos = None
        player_state = model.PlayerState.WD
    if to_model:
        return value.ScrappedPlayer(name=_tokenise(name),
                                    player_module=mens_players,
                                    total=None,
                                    position=pos,
                                    player_state=player_state,
                                    round_scores=rds,
                                    missing_writer=missing_player_writer)
    else:
        return {
            'name': _tokenise(name),
            'player_module': mens_players,
            'total': None,
            'position': pos,
            'player_state': player_state,
            'round_scores': rds
        }


def _to_int(pos: Union[str, int]):
    if isinstance(pos, int) or not pos:
        return pos
    if pos.isnumeric():
        return int(pos)
    # logger.debug(f"POS: {pos}")
    if "CUT" in pos:
        return pos
    if "WD" in pos:
        return pos
    if "T" in pos:
        return int(pos.replace('T', ''))


def _extract_value(table, pos, cell_id, none_tst):
    val = table[pos]['csvw:cells'][cell_id]['csvw:value']
    return val if val != none_tst else None


def _tokenise(name):
    if name[-1] in ["I", "."]:
        parts = name.split(' ')
        first_parts = parts[0:-1]
        return ' '.join(first_parts) + "_" + parts[-1]
    return name


def _write_file(file_name, content):
    with open(f"{file_name}", 'w') as f:
        f.write(content)
