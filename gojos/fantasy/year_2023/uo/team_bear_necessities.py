import sys
from gojos.fantasy.teams import *
from gojos.fantasy import helpers
from gojos.players.mens_players import *

this = sys.modules[__name__]

TEAM = TeamBearNecessities


def team_bear_necessities(major):
    helpers.selection_fn_caller(this, major)
    return TEAM

def selection(major):
    TEAM.major(major).selection(McIlroy)
    TEAM.major(major).selection(Scheffler)


def wildcards(major):
    pass
