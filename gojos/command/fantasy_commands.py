from functools import reduce, partial


def cut_danger(fantasy_teams):
    return _assess_cut_danger(fantasy_teams)


def _assess_cut_danger(fantasy_teams):
    return reduce(_cut_danger_for_team, fantasy_teams, {})


def _cut_danger_for_team(accum, team):
    return {**accum, **{team: team.players_relative_to_cut()}}
