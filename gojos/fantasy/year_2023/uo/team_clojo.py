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
    """
    Add 10 teams to your roster.

    An example of adding Rory to your roster is:
    TEAM.major(major).selection(McIlroy)
    """
    TEAM.major(major).add_to_roster(McIlroy)
    TEAM.major(major).add_to_roster(Scheffler)
    TEAM.major(major).add_to_roster(Rose)
    TEAM.major(major).add_to_roster(Rahm)
    TEAM.major(major).add_to_roster(Hovland)
    TEAM.major(major).add_to_roster(Day)
    TEAM.major(major).add_to_roster(Schauffele)
    TEAM.major(major).add_to_roster(Theegala)
    TEAM.major(major).add_to_roster(Burns)
    TEAM.major(major).add_to_roster(Spieth)


def wildcards(major):
    """
    You get 4 wildcards for the tournament.  A wild card allows you to trade out a player in your selections
    and trade in a new player.  The trade occurs from a specific round.

    The following is an example of trading out Scottie and replacing him with Colin from round 3.

    TEAM.major(major).wildcard(WildCard().from_round(3).trade_out(Scheffler).trade_in(Morikawa))
    """
    pass
