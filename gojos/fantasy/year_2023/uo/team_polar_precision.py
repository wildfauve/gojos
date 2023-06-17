import sys
from gojos.fantasy.teams import *
from gojos.fantasy import helpers
from gojos.players.mens_players import *
from gojos.model.fantasy import WildCard

this = sys.modules[__name__]

TEAM = TeamPolarPrecision

def team_polar_precision(major):
    helpers.selection_fn_caller(this, major)
    return TEAM


def selection(major):
    """
    Add 10 teams to your roster.

    An example of adding Rory to your roster is:
    TEAM.major(major).selection(McIlroy)
    """

    TEAM.major(major).on_roster(McIlroy)
    TEAM.major(major).on_roster(Matsuyama)
    TEAM.major(major).on_roster(Fleetwood)
    TEAM.major(major).on_roster(Scheffler)
    TEAM.major(major).on_roster(Rose)
    TEAM.major(major).on_roster(Rahm)
    TEAM.major(major).on_roster(Hovland)
    TEAM.major(major).on_roster(Fitzpatrick)
    TEAM.major(major).on_roster(Homa)
    TEAM.major(major).on_roster(Hatton)

def wildcards(major):
    """
    You get 4 wildcards for the tournament.  A wild card allows you to trade out a player in your selections
    and trade in a new player.  The trade occurs from a specific round.

    The following is an example of trading out Scottie and replacing him with Colin from round 3.

    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(Scheffler).trade_in(Morikawa))
    """

    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(Homa).trade_in(Fowler))
    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(Rahm).trade_in(Clark))
    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(Rose).trade_in(Schauffele))

    
    pass
