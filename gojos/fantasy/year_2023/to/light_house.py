import sys
from gojos.fantasy.teams import *
from gojos.fantasy import helpers
from gojos.players import mens_players as players
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
    TEAM.major(major).on_roster(players.McIlroy)
    """
    TEAM.major(major).on_roster(players.McIlroy)
    TEAM.major(major).on_roster(players.Fleetwood)
    TEAM.major(major).on_roster(players.Smith)
    TEAM.major(major).on_roster(players.Lowry)
    TEAM.major(major).on_roster(players.Hatton)
    TEAM.major(major).on_roster(players.Kim_T)
    TEAM.major(major).on_roster(players.Koepka)
    TEAM.major(major).on_roster(players.Rahm)
    TEAM.major(major).on_roster(players.Scheffler)
    TEAM.major(major).on_roster(players.Hojgaard_N)
    pass

def wildcards(major):
    """
    You get 4 wildcards for the tournament.  A wild card allows you to trade out a player in your selections
    and trade in a new player.  The trade occurs from a specific round.

    The following is an example of trading out Scottie and replacing him with Colin from round 3.

    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(players.Scheffler).trade_in(players.Morikawa))
    """
    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(players.Lowry).trade_in(players.Harman))
    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(players.Koepka).trade_in(players.Spieth))
    TEAM.major(major).play_wildcard(WildCard().from_round(4).trade_out(players.Scheffler).trade_in(players.Hovland))
    TEAM.major(major).play_wildcard(WildCard().from_round(4).trade_out(players.Smith).trade_in(players.Day))
    pass


