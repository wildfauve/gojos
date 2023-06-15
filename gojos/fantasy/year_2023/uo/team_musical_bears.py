import sys
from gojos.fantasy.teams import *
from gojos.fantasy import helpers
from gojos.players.mens_players import *

this = sys.modules[__name__]

TEAM = TeamMusicalBears

def team_musical_bears(major):
    helpers.selection_fn_caller(this, major)
    return TEAM


def selection(major):
    """
    Add 10 teams to your roster.

    An example of adding Rory to your roster is:
    TEAM.major(major).selection(McIlroy)
    """
    TEAM.major(major).selection(Scheffler)
    TEAM.major(major).selection(McIlroy)
    TEAM.major(major).selection(Morikawa)
    TEAM.major(major).selection(Fowler)
    TEAM.major(major).selection(Hovland)
    TEAM.major(major).selection(Thomas)
    TEAM.major(major).selection(Theegala)
    TEAM.major(major).selection(Rahm)
    TEAM.major(major).selection(Kitayama)
    TEAM.major(major).selection(Young_Cam)


def wildcards(major):
    """
    You get 4 wildcards for the tournament.  A wild card allows you to trade out a player in your selections
    and trade in a new player.  The trade occurs from a specific round.

    The following is an example of trading out Scottie and replacing him with Colin from round 3.

    TEAM.major(major).wildcard(WildCard().from_round(3).trade_out(Scheffler).trade_in(Morikawa))
    """
    pass

