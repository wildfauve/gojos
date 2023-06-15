from enum import Enum
from functools import partial

from rich.table import Table

from gojos.model.player import Player

from gojos.util import fn, identity


class Team:
    def __init__(self, name, members):
        self.name = name
        self.symbolic_name = name.replace(" ", "")
        self.members = members
        self.fantasy_tournament = None

    def major(self, tournament):
        if self.fantasy_tournament:
            return self.fantasy_tournament
        self.fantasy_tournament = FantasyTournament(tournament, self)
        return self.fantasy_tournament

    def points_per_round(self):
        return self.fantasy_tournament.points_per_round()

    def total_points(self, for_round=None):
        return sum([fantasy_draw.total_points(for_round) for fantasy_draw in self.fantasy_draws])

    def explain_points(self):
        return [fantasy_draw.explain_points() for fantasy_draw in self.fantasy_draws]

    def __hash__(self):
        return hash((self.symbolic_name,))

    def __eq__(self, other):
        return self.symbolic_name == other.symbolic_name


class FantasyTournament:
    def __init__(self, tournament, team):
        self.team = team
        self.tournament = tournament
        self.roster = []
        self.wild_card_swaps = []

    def on_roster(self, player=None):
        if not player:
            return self
        if self.tournament.points_strategy.valid_for_roster(self.roster, player):
            self.roster.append(RosterPlayer(tournament=self.tournament, player=player))
        else:
            breakpoint()
        return self

    def wildcard(self, wildcard):
        if self.tournament.points_strategy.valid_wildcard(self.wild_card_swaps, wildcard):
            self.wild_card_swaps.append(wildcard)
        else:
            breakpoint()
        return self

    def show(self, table: Table, for_round: int = None):
        if for_round:
            for mt_id, selection in self.match_selections[1].items():
                selection.show(self.draw.name, table)
        else:
            for rd_id, matches in self.match_selections.items():
                for mt_id, selection in matches.items():
                    selection.show(self.draw.name, table)

    def points_per_round(self):
        pts_per_player_per_rd = [selects.points_per_round(self.wild_card_swaps) for selects in self.roster]
        print(f"Team: {self.team.name}...{pts_per_player_per_rd}")
        if len(pts_per_player_per_rd) == 1:  # there is only 1 player
            return pts_per_player_per_rd[0]
        total = [sum(rd_pts) for rd_pts in zip(*pts_per_player_per_rd)]
        print(f"Team: {self.team.name}...TOTAL:  {total}")
        return total

    def total_points(self, for_round=None):
        if for_round:
            if for_round not in self.match_selections.keys():
                return 0
            return sum([sel.points() for sel in self.match_selections[for_round].values()])
        return sum([sel.points() for selections in self.match_selections.values() for sel in selections.values()])

    def explain_points(self):
        return {
            "event": self.draw.name,
            "matches": [sel.explain_points() for selections in self.match_selections.values() for sel in
                        selections.values()]
        }

    def match(self, match_id):
        rd_id, mt_id = identity.split_match_id(match_id)
        selection = self._find_match_selection(rd_id, mt_id)
        if not selection:
            selection = RosterPlayer(self.draw, rd_id, mt_id)
            self._add_selection(selection, rd_id, mt_id)
        return selection

    def selection_for(self, round_id, match_id):
        return self._find_match_selection(round_id, match_id)

    def _add_selection(self, selection, round_id, match_id):
        if not self.match_selections.get(round_id):
            self.match_selections[round_id] = {}
        self.match_selections[round_id][match_id] = selection
        return self

    def _find_match_selection(self, round_id, match_id):
        return fn.deep_get(self.match_selections, [round_id, match_id])


class RosterPlayer:
    def __init__(self, tournament, player):
        self.tournament = tournament
        self.player = player
        self.points_strategy = tournament.points_strategy
        self.per_round_accum_strategy = tournament.round_factor_strategy

    def points_per_round(self, wildcards):
        return self.points_strategy.calc(self, wildcards=wildcards, explain=False)

    def explain_points(self):
        if not self.match.is_finished():
            return {
                "match": self.match.match_id,
                "between": f"{self.match.player1.player().name}, {self.match.player2.player().name}" if self.match.has_draw() else None,
                "result-winner": "Not Finished",
                "selected-winner": self.selected_winner.player().name if self.selected_winner else None,
                "selected-in-sets": self.in_number_sets if self.in_number_sets else None,
                "points": []
            }

        return {
            "match": self.match.match_id,
            "between": f"{self.match.player1.player().name}, {self.match.player2.player().name}",
            "result-winner": self.match.match_winner.player().name,
            "result-in-sets": self.match.number_of_sets_played(),
            "selected-winner": self.selected_winner.player().name if self.selected_winner else None,
            "selected-in-sets": self.in_number_sets if self.in_number_sets else None,
            "points": self.points_strategy.calc(self, explain=True)
        }

    def show(self, draw_name: str, table: Table):
        table.add_row(draw_name,
                      self.match.match_id,
                      self.match.match_block(),
                      self.selected_winner.player().name,
                      str(self.in_number_sets))


class WildCard:

    @classmethod
    def has_swap(cls, wildcards, selected_player, for_round):
        if not wildcards:
            return None
        wc = list(fn.select(partial(cls._rd_player_predicate, selected_player, for_round), wildcards))
        if not wc:
            return None
        if len(wc) > 1:
            return sorted(wc, key=lambda x: x.starting_at_round)[-1]
        return wc[0]

    @classmethod
    def _rd_player_predicate(cls, selected_player, for_round, wildcard_swap):
        return ((selected_player == wildcard_swap.trade_out_player or
                 selected_player == wildcard_swap.trade_in_player) and
                wildcard_swap.starting_at_round <= for_round)

    def __init__(self):
        self.starting_at_round = None
        self.trade_out_player = None
        self.trade_in_player = None

    def from_round(self, at_round):
        self.starting_at_round = at_round
        return self

    def __repr__(self):
        return f"Wildcard(starting_at_round={self.starting_at_round}, trade_out={self.trade_out_player.name} trade_in={self.trade_in_player.name})"
    def trade_out(self, player):
        self.trade_out_player = player
        return self

    def trade_in(self, player):
        self.trade_in_player = player
        return self
