from gojos.players.mens_players import *

def round_1(tournie):
    return [
        tournie.leaderboard.for_round(1).player(McIlroy).score(70)
    ]
