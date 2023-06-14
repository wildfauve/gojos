import re

def selection_fn_caller(team_module, tournament):
    [getattr(team_module, f)(tournament) for f in dir(team_module) if re.match(f"^selection_", f)]