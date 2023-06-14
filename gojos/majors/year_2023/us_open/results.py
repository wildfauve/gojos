from gojos.players.mens_players import *

def round_1(tournie):
    return [
        tournie.leaderboard.for_round(1).player(McIlroy).score(70).position(1),
        tournie.leaderboard.for_round(1).player(Scheffler).score(72).position(4),
    ]


def round_2(tournie):
    return [
        tournie.leaderboard.for_round(2).player(McIlroy).score(68).position(2),
        tournie.leaderboard.for_round(2).player(Scheffler).score(62).position(1),
    ]
