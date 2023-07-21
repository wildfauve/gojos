from typing import Tuple, Union
from functools import reduce, partial
import json

from csvw import CSVW

import requests
from bs4 import BeautifulSoup

from gojos.players import mens_players
from gojos import model
from gojos.util import fn

from . import value

leaderboard = "https://www.pgatour.com/leaderboard"


def build_leaderboard(for_round: int, to_model: bool = True):
    return _csvw_parser(_entries(_get_page(leaderboard)), for_round, to_model)


def _get_page(url_or_file):
    if 'http' in url_or_file:
        return BeautifulSoup(requests.get(url_or_file).text, "html.parser")
    return BeautifulSoup(open(url_or_file, encoding='UTF-8'), "html.parser")


def _entries(page):
    return page.find('script', type='application/ld+json').text


def _csvw_parser(json_ld, for_round, to_model):
    data = json.loads(json_ld)
    num_players = len(data['mainEntity']['csvw:tableSchema']['csvw:columns'][1]['csvw:cells'])
    return [_per_player_row(for_round, data['mainEntity']['csvw:tableSchema']['csvw:columns'], idx, to_model) for idx in
            range(0, num_players - 1)]
    # return reduce(partial(_per_player_row, for_round, data['mainEntity']['csvw:tableSchema']['csvw:columns']),
    #               range(0, num_players - 1), [])


def _per_player_row(for_round, table, cell_id, to_model):
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
                                    round_scores=rds)
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
    if "CUT" in pos:
        return pos
    if "WD" in pos:
        return pos
    if "T" in pos:
        return int(pos.replace('T', ''))
    if pos.isnumeric():
        return int(pos)
    breakpoint()


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
