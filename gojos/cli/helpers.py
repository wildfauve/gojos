from gojos import model

# Tournaments = model.tournament.tournaments()

Teams = model.fantasy.teams()

# def tournament_names():
#     return Tournaments.slam_symbols()
#
#
# def to_tournament(name):
#     return Tournaments.slam(name)
#

def symbolised_names():
    return Teams.symbolic_names()
