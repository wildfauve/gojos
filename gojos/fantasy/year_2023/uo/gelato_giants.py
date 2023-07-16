import sys
from gojos.fantasy.teams import *
from gojos.fantasy import helpers
from gojos.players import mens_players as players
from gojos.model.fantasy import WildCard

this = sys.modules[__name__]

TEAM = None


def team():
    this.TEAM = model.Team.get('Gelato Giants')


def team_gelato_giants(major):
    team()
    helpers.selection_fn_caller(this, major)
    return TEAM



def selection(major):
    """
    Add 10 teams to your roster.

    An example of adding Rory to your roster is:
    TEAM.major(major).selection(players.McIlroy)
    """

    TEAM.major(major).on_roster(players.McIlroy)
    TEAM.major(major).on_roster(players.Finau)
    TEAM.major(major).on_roster(players.Fleetwood)
    TEAM.major(major).on_roster(players.Scheffler)
    TEAM.major(major).on_roster(players.Rose)
    TEAM.major(major).on_roster(players.Rahm)
    TEAM.major(major).on_roster(players.Hovland)
    TEAM.major(major).on_roster(players.Molinari)
    TEAM.major(major).on_roster(players.Homa)
    TEAM.major(major).on_roster(players.Taylor)

def wildcards(major):
    """
    You get 4 wildcards for the tournament.  A wild card allows you to trade out a player in your selections
    and trade in a new player.  The trade occurs from a specific round.

    The following is an example of trading out Scottie and replacing him with Colin from round 3.

    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(players.Scheffler).trade_in(players.Morikawa))
    """

    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(players.Homa).trade_in(players.Fowler))
    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(players.Taylor).trade_in(players.Clark))
    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(players.Rose).trade_in(players.Schauffele))
    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(players.Molinari).trade_in(players.Bennett))
    
    pass

