from typing import Tuple
import csv

from gojos import model, graph
from gojos.util import monad
from gojos.players import mens_players

from . import helpers, commanda


@commanda.command(graph_names=['tournament'])
def new_tournament(tournament_name, perma_id, subject_name) -> monad.EitherMonad[model.GrandSlam]:
    tournie = model.GrandSlam.create(name=tournament_name, subject_name=subject_name, perma_id=perma_id)
    if not tournie:
        breakpoint()
    return monad.Right(tournie)


@commanda.command(['tournament'])
def new_event(tournament, year):
    ev = tournament.make_event(year)

    if not ev:
        breakpoint()
    return monad.Right(ev)



@commanda.command(graph_names=['tournament'])
def add_entries(tournament, year):
    event = tournament.for_year(year, load=True)

    if not event:
        return monad.Left(event)

    event.build_entry_list()

    return monad.Right(event)


@commanda.command(graph_names=['tournament'])
def leaderboard_for_round(tournament, year, for_round):
    event = tournament.for_year(year, load=True)

    rd_results = event.scores_for_round(for_round=for_round)
    breakpoint()
    return monad.Right(event)


@commanda.command2(graphs=['tournament', 'players'])
def leaderboard_for_round2(tournament_graph, players_graph, tournament, year, for_round):
    result = graph.add_round_scores(tournament_graph, players_graph, tournament, year, for_round)
    breakpoint()
    event = tournament.for_year(year, load=True)

    rd_results = event.scores_for_round(for_round=for_round)
    breakpoint()
    return monad.Right(event)
