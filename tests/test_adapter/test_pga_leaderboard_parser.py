import json

import requests_mock
from jinja2 import Environment, FileSystemLoader

from gojos import adapter

environment = Environment(loader=FileSystemLoader("tests/fixtures/templates/"))


class MissingPlayers:
    def __init__(self):
        self.missing_players = []

    def missing(self, player_def):
        self.missing_players.append(player_def)
        return self


def test_scrap_no_missing_players(configure_repo, build_players, empty_leaderboard_html):
    missing_writer = MissingPlayers()
    with requests_mock.Mocker() as m:
        m.get('https://www.pgatour.com/leaderboard', text=empty_leaderboard_html)
        adapter.pga_leaderboard_parser.build_leaderboard(for_round=1, missing_player_writer=missing_writer.missing)
        assert not missing_writer.missing_players


def test_scrap_r1_scores(configure_repo, build_players, r1_leaderboard_html):
    missing_writer = MissingPlayers()

    expected_scores = [('Fleetwood', '66'),
                       ('Morikawa', '67'),
                       ('Scheffler', '68'),
                       ('Fitzpatrick', '69'),
                       ('Rahm', '70'),
                       ('Hovland', '71'),
                       ('Hatton', '72'),
                       ('Homa', '73'),
                       ('Schauffele', '74'),
                       ('McIlroy', '75'),
                       ('Finau', '76')]

    with requests_mock.Mocker() as m:
        m.get('https://www.pgatour.com/leaderboard', text=r1_leaderboard_html)
        results = adapter.pga_leaderboard_parser.build_leaderboard(for_round=1,
                                                                   missing_player_writer=missing_writer.missing)

        player_scores = [(p.player_klass.klass_name, p.round_scores['this']) for p in results]

        assert player_scores == expected_scores


