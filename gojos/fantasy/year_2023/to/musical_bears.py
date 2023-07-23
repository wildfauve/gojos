import sys
from gojos.fantasy.teams import *
from gojos.fantasy import helpers
from gojos.players import mens_players as players
from gojos.model.fantasy import WildCard

this = sys.modules[__name__]

TEAM = None


def team():
    this.TEAM = model.Team.get('Musical Bears')


def team_musical_bears(major):
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
    TEAM.major(major).on_roster(players.Cantlay)
    TEAM.major(major).on_roster(players.Fowler)
    TEAM.major(major).on_roster(players.Hatton)
    TEAM.major(major).on_roster(players.Burns)
    TEAM.major(major).on_roster(players.Schauffele)
    TEAM.major(major).on_roster(players.Homa)
    TEAM.major(major).on_roster(players.Rahm)
    TEAM.major(major).on_roster(players.Scheffler)
    TEAM.major(major).on_roster(players.Clark)

    pass

def wildcards(major):
    """
    You get 4 wildcards for the tournament.  A wild card allows you to trade out a player in your selections
    and trade in a new player.  The trade occurs from a specific round.

    The following is an example of trading out Scottie and replacing him with Colin from round 3.

    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(players.Scheffler).trade_in(players.Morikawa))
    """
    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(players.Burns).trade_in(players.Harman))
    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(players.Cantlay).trade_in(players.Fleetwood))
    TEAM.major(major).play_wildcard(WildCard().from_round(4).trade_out(players.Scheffler).trade_in(players.Hovland))
    TEAM.major(major).play_wildcard(WildCard().from_round(4).trade_out(players.Hatton).trade_in(players.Straka))
    pass
