import sys
from gojos.fantasy.teams import *
from gojos.fantasy import helpers
from gojos.players.mens_players import *

this = sys.modules[__name__]

TEAM = TeamHeroHangouts

def team_hero_hangouts(major):
    helpers.selection_fn_caller(this, major)
    return TEAM


def selection_precut(major):
    TEAM.major(major).precut_selection(McIlroy)


