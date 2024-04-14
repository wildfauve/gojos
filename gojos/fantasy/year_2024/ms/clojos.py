import sys
from gojos.fantasy.teams import *
from gojos.fantasy import helpers
from gojos.players import mens_players as players
from gojos.model.fantasy import WildCard

this = sys.modules[__name__]

TEAM = None


def team():
    this.TEAM = model.Team.get('Clojos')


def team_clojos(major):
    team()
    helpers.selection_fn_caller(this, major)
    return TEAM


def selection(major):
    """
    Add 10 teams to your roster.

    An example of adding Rory to your roster is:
    TEAM.major(major).on_roster(players.McIlroy)
    """
    TEAM.major(major).on_roster(players.McIlroy)
    TEAM.major(major).on_roster(players.Lowry)
    TEAM.major(major).on_roster(players.Rahm)
    TEAM.major(major).on_roster(players.Finau)
    TEAM.major(major).on_roster(players.Scheffler)
    TEAM.major(major).on_roster(players.Cantlay)
    TEAM.major(major).on_roster(players.Lowry)
    TEAM.major(major).on_roster(players.Fleetwood)
    TEAM.major(major).on_roster(players.Schauffele)
    TEAM.major(major).on_roster(players.Koepka)
    pass

def wildcards(major):
    """
    You get 4 wildcards for the tournament.  A wild card allows you to trade out a player in your selections
    and trade in a new player.  The trade occurs from a specific round.

    The following is an example of trading out Scottie and replacing him with Colin from round 3.

    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(players.Scheffler).trade_in(players.Morikawa))
    """
    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(players.Finau).trade_in(players.DeChambeau))
    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(players.Rahm).trade_in(players.Homa))
    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(players.Koepka).trade_in(players.Morikawa))
    TEAM.major(major).play_wildcard(WildCard().from_round(4).trade_out(players.Lowry).trade_in(players.Davis))
    pass
