import re


def apply_selections(fantasy_module, tournament):
    return [_apply_selections(fantasy_module, team_fn, tournament) for team_fn in
            _apply_functions_for_teams(fantasy_module)]


def _apply_functions_for_teams(fantasy_module):
    return [f for f in dir(fantasy_module) if re.match("^team_", f)]


def _apply_selections(fantasy_module, team_fn, tournament):
    return getattr(fantasy_module, team_fn)(tournament)
