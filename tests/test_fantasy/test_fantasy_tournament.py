from gojos import model
from gojos.players import mens_players as players

from tests.shared import tournament

def setup_function():
    model.Team.reset()

def test_create_fantasy_tournament(configure_repo, build_players):
    team = create_team()

    event = tournament.clojos_open_2023()

    fantasy = team.major(event)

    assert fantasy.event == event
    assert not fantasy.roster
    assert not fantasy.wildcard_trades

    fantasy.on_roster(players.McIlroy)
    fantasy.on_roster(players.Rahm)
    fantasy.on_roster(players.Finau)
    wc = model.WildCard().from_round(3).trade_out(players.Rahm).trade_in(players.Homa)
    fantasy.play_wildcard(wc)

    assert {r.player for r in fantasy.roster} == {players.McIlroy, players.Rahm, players.Finau}

    wc = {(wc.trade_out_player, wc.trade_in_player, wc.starting_at_round) for wc in fantasy.wildcard_trades}

    assert wc == {(players.Rahm, players.Homa, 3)}




def create_team():
    return model.Team.create("Fauve", "Perky, Jacque, Albert", features=[])

