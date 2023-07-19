from gojos import model
from gojos.players import mens_players


def round_1(event):
    round1 = event.leaderboard.for_round(1) 
    round1.player_score(mens_players.Morikawa, 65)
    round1.player_score(mens_players.Finau, 66)
    round1.player_score(mens_players.Fleetwood, 67)
    round1.player_score(mens_players.Scheffler, 68)
    round1.player_score(mens_players.Fitzpatrick, 69)
    round1.player_score(mens_players.Rahm, 70)
    round1.player_score(mens_players.Hovland, 71)
    round1.player_score(mens_players.Hatton, 72)
    round1.player_score(mens_players.Homa, 73)
    round1.player_score(mens_players.Schauffele, 74)
    round1.done()
    
def round_2(event):
    round2 = event.leaderboard.for_round(2)
    round2.player_score(mens_players.Morikawa, 72)
    round2.player_score(mens_players.Finau, 76)
    round2.player_score(mens_players.Fleetwood, 62)
    round2.player_score(mens_players.Scheffler, 69)
    round2.player_score(mens_players.Fitzpatrick, 70)
    round2.player_score(mens_players.Rahm, 70)
    round2.player_score(mens_players.Hovland, 67)
    round2.player_score(mens_players.Hatton, 70)
    round2.player_score(mens_players.Homa, 68)
    round2.player_score(mens_players.Schauffele, 61)
    round2.done()

def round_3(event):
    round3 = event.leaderboard.for_round(3)
    round3.player_score(mens_players.Morikawa, 70)
    round3.player_score(mens_players.Finau, 69)
    round3.player_score(mens_players.Fleetwood, None, state=model.PlayerState.CUT)
    round3.player_score(mens_players.Scheffler, 71)
    round3.player_score(mens_players.Fitzpatrick, 72)
    round3.player_score(mens_players.Rahm, 74)
    round3.player_score(mens_players.Hovland, 75)
    round3.player_score(mens_players.Hatton, 69)
    round3.player_score(mens_players.Homa, 68)
    round3.player_score(mens_players.Schauffele, 72)
    round3.done()

def round_2_with_mc(event):
    round2 = event.leaderboard.for_round(2)
    round2.player_score(mens_players.Morikawa, 72)
    round2.player_score(mens_players.Finau, 76)
    round2.player_score(mens_players.Fleetwood, 77, state=model.PlayerState.CUT)
    round2.player_score(mens_players.Scheffler, 69)
    round2.player_score(mens_players.Fitzpatrick, 70)
    round2.player_score(mens_players.Rahm, 70)
    round2.player_score(mens_players.Hovland, 67)
    round2.player_score(mens_players.Hatton, 70)
    round2.player_score(mens_players.Homa, 68)
    round2.player_score(mens_players.Schauffele, 61)
    round2.done()