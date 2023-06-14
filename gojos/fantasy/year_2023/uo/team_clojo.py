import sys
from gojos.fantasy.teams import *
from gojos.fantasy import helpers
from gojos.players.mens_players import *

this = sys.modules[__name__]

TEAM = TeamClojo


def team_clojo(major):
    helpers.selection_fn_caller(this, major)
    return TEAM


def selection(major):
    TEAM.major(major).selection(McIlroy)


def wildcards(major):
    pass
