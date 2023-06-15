import sys
from gojos.fantasy.teams import *
from gojos.fantasy import helpers
from gojos.players.mens_players import *

this = sys.modules[__name__]

TEAM = TeamLightHouse


def team_light_house(major):
    helpers.selection_fn_caller(this, major)
    return TEAM


def selection(major):
    """
    Add 10 teams to your roster.

    An example of adding Rory to your roster is:
    TEAM.major(major).selection(McIlroy)
    """
    TEAM.major(major).add_to_roster(Scheffler)
    TEAM.major(major).add_to_roster(Morikawa)
    TEAM.major(major).add_to_roster(Finau)
    TEAM.major(major).add_to_roster(Fitzpatrick)
    TEAM.major(major).add_to_roster(Thomas)
    TEAM.major(major).add_to_roster(Wu)
    TEAM.major(major).add_to_roster(Spieth)
    TEAM.major(major).add_to_roster(Conners)
    TEAM.major(major).add_to_roster(Scott)
    TEAM.major(major).add_to_roster(Rose)


def wildcards(major):
    """
    You get 4 wildcards for the tournament.  A wild card allows you to trade out a player in your selections
    and trade in a new player.  The trade occurs from a specific round.

    The following is an example of trading out Scottie and replacing him with Colin from round 3.

    TEAM.major(major).wildcard(WildCard().from_round(3).trade_out(Scheffler).trade_in(Morikawa))
    """
    pass


