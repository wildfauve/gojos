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



@commanda.command(graph_names=['tournament'])
def add_entries(tournament, year):
    event = tournament.for_year(year, load=True)

    if not event:
        return monad.Left(event)

    event.build_entry_list()

    return monad.Right(event)


@commanda.command(graph_names=['tournament'])
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


@commanda.command(graph_names=['tournament'])
def leaderboard_for_round(tournament, year, for_round):
    event = tournament.for_year(year, load=True)

    rd_results = event.scores_for_round(for_round=for_round)
    breakpoint()
    return monad.Right(event)
