import sys
from gojos.fantasy.teams import *
from gojos.fantasy import helpers
from gojos.players.mens_players import *

this = sys.modules[__name__]

TEAM = TeamGelatoGiants

def team_gelato_giants(major):
    helpers.selection_fn_caller(this, major)
    return TEAM


def selection(major):
    TEAM.major(major).selection(McIlroy)


def wildcards(major):
    pass


