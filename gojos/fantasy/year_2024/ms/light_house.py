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
    TEAM.major(major).on_roster(players.Clark)
    TEAM.major(major).on_roster(players.Burns)
    TEAM.major(major).on_roster(players.Højgaard)
    TEAM.major(major).on_roster(players.Scheffler)
    TEAM.major(major).on_roster(players.Finau)
    TEAM.major(major).on_roster(players.Hovland)
    TEAM.major(major).on_roster(players.Aberg)
    TEAM.major(major).on_roster(players.Fleetwood)
    TEAM.major(major).on_roster(players.Koepka)
    pass

def wildcards(major):
    """
    You get 4 wildcards for the tournament.  A wild card allows you to trade out a player in your selections
    and trade in a new player.  The trade occurs from a specific round.

    The following is an example of trading out Scottie and replacing him with Colin from round 3.

    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(players.Scheffler).trade_in(players.Morikawa))
    """
    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(players.Hovland).trade_in(players.DeChambeau))
    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(players.Clark).trade_in(players.Smith_Ca))
    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(players.Burns).trade_in(players.Morikawa))
    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(players.Finau).trade_in(players.Homa))
    pass


