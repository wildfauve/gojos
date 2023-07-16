import sys
from gojos.fantasy.teams import *
from gojos.fantasy import helpers
from gojos.players.mens_players import *
from gojos.model.fantasy import WildCard

this = sys.modules[__name__]

TEAM = None


def team():
    this.TEAM = model.Team.get('LightHouse')


def team_lighthouse(major):
    team()
    helpers.selection_fn_caller(this, major)
    return TEAM


def selection(major):
    """
    Add 10 teams to your roster.

    An example of adding Rory to your roster is:
    TEAM.major(major).selection(McIlroy)
    """
    TEAM.major(major).on_roster(Scheffler)
    TEAM.major(major).on_roster(Morikawa)
    TEAM.major(major).on_roster(Finau)
    TEAM.major(major).on_roster(Fitzpatrick)
    TEAM.major(major).on_roster(Thomas)
    TEAM.major(major).on_roster(Wu)
    TEAM.major(major).on_roster(Spieth)
    TEAM.major(major).on_roster(Conners)
    TEAM.major(major).on_roster(Scott)
    TEAM.major(major).on_roster(Rose)


def wildcards(major):
    """
    You get 4 wildcards for the tournament.  A wild card allows you to trade out a player in your selections
    and trade in a new player.  The trade occurs from a specific round.

    The following is an example of trading out Scottie and replacing him with Colin from round 3.

    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(Scheffler).trade_in(Morikawa))
    """
    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(Rose).trade_in(McIlroy))
    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(Thomas).trade_in(Fowler))
    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(Spieth).trade_in(Kim_S_W))
    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(Scott).trade_in(Schauffele))
    pass


