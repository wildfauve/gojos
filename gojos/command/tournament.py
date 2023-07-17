from typing import Tuple
import csv

from gojos import model
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


@commanda.command()
def new_draw(tournament, year, draw_name, best_of, draw_size, fantasy_pt_strat: Tuple = None):
    event = tournament.for_year(year, load=True)
    if not event:
        return monad.Left(event)

    draw = event.make_draw(name=draw_name,
                           best_of=best_of,
                           draw_size=draw_size,
                           points_strategy_components=fantasy_pt_strat)

    if draw:
        draw.init_draw()
        return monad.Right(draw)


@commanda.command()
def add_entries(tournament, year, draw_name, in_file):
    event = tournament.for_year(year, load=True)

    if not event:
        return monad.Left(event)

    draw = model.Draw.get(event=event, name=draw_name)
    entries = []
    with open(in_file, newline='') as f:
        reader = csv.reader(f, delimiter=',')
        for player_klass_name, seed in reader:
            player = _get_player(draw_name, player_klass_name)
            if not player:
                breakpoint()
            # if "Wang" in player.klass_name:
            #     breakpoint()
            entries.append((player, seed))
    draw.add_entries(entries)
    return monad.Right(draw)


@commanda.command()
def first_round_draw(tournament, year, draw_name, in_file):
    event = tournament.for_year(year, load=True)

    if not event:
        return monad.Left(event)

    draw = model.Draw.get(event=event, name=draw_name)

    first_rd = []
    with open(in_file, newline='') as f:
        reader = csv.reader(f, delimiter=',')
        for match, pl1_klass_name, pl2_klass_name in reader:
            pl1 = _get_player(draw_name, pl1_klass_name)
            pl2 = _get_player(draw_name, pl2_klass_name)
            if not pl1 or not pl2:
                breakpoint()
            first_rd.append((int(match), pl1, pl2))

    draw.first_round_draw(first_rd)
    return monad.Right(draw)


@commanda.command()
def results(tournament, year, round_number, scores_only):
    event = tournament.for_year(year, load=True)

    rd_results = model.results(event=event,
                               for_round=round_number,
                               scores_only=scores_only)
    return monad.Right(event)


def _get_player(draw_name, player_klass_name):
    if draw_name == "MensSingles":
        return getattr(atp_players, player_klass_name, None)
    return getattr(wta_players, player_klass_name, None)
