import sys
from gojos.fantasy.teams import *
from gojos.fantasy import helpers
from gojos.players import mens_players as players
from gojos.model.fantasy import WildCard

this = sys.modules[__name__]

TEAM = None


def team():
    this.TEAM = model.Team.get('Hero Hangouts')


def team_hero_hangouts(major):
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
    TEAM.major(major).on_roster(players.Bhatia)
    TEAM.major(major).on_roster(players.Glover)
    TEAM.major(major).on_roster(players.Harman)
    TEAM.major(major).on_roster(players.Scheffler)
    TEAM.major(major).on_roster(players.Homa)
    TEAM.major(major).on_roster(players.Fitzpatrick_M)
    TEAM.major(major).on_roster(players.Aberg)
    TEAM.major(major).on_roster(players.Fleetwood)
    TEAM.major(major).on_roster(players.Willett)
    pass

def wildcards(major):
    """
    You get 4 wildcards for the tournament.  A wild card allows you to trade out a player in your selections
    and trade in a new player.  The trade occurs from a specific round.

    The following is an example of trading out Scottie and replacing him with Colin from round 3.

    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(players.Scheffler).trade_in(players.Morikawa))
    """
    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(players.McIlroy).trade_in(players.Højgaard))
    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(players.Harman).trade_in(players.Davis))
    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(players.Bhatia).trade_in(players.Morikawa))
    TEAM.major(major).play_wildcard(WildCard().from_round(3).trade_out(players.Fleetwood).trade_in(players.DeChambeau))
    
    pass


