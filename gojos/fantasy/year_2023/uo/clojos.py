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
    TEAM.major(major).selection(players.McIlroy)
    """
    TEAM.major(major).on_roster(players.McIlroy)
    TEAM.major(major).on_roster(players.Scheffler)
    TEAM.major(major).on_roster(players.Rose)
    TEAM.major(major).on_roster(players.Rahm)
    TEAM.major(major).on_roster(players.Hovland)
    TEAM.major(major).on_roster(players.Day)
    TEAM.major(major).on_roster(players.Schauffele)
    TEAM.major(major).on_roster(players.Theegala)
    TEAM.major(major).on_roster(players.Burns)
    TEAM.major(major).on_roster(players.Spieth)


def wildcards(major):
    """
    You get 4 wildcards for the tournament.  A wild card allows you to trade out a player in your selections
    and trade in a new player.  The trade occurs from a specific round.

    The following is an example of trading out Scottie and replacing him with Colin from round 3.

    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(players.Scheffler).trade_in(players.Morikawa))
    """
    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(players.Rose).trade_in(players.Fowler))
    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(players.Day).trade_in(players.Johnson))
    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(players.Spieth).trade_in(players.Clark))
    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(players.Theegala).trade_in(players.Kim_T))
    pass
