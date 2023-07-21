import click

from gojos import command, presenter
from gojos.majors import tournaments

from gojos.initialiser import environment, db

from . import helpers

def tournament_names():
    return tournaments.tournament_names()


@click.group()
def cli():
    pass


@click.command()
@click.option("--tournament", "-t")
@click.option("--subject-name", "-s")
@click.option("--perma-id", "-p")
def new_tournament(tournament, perma_id, subject_name):
    """
    """
    command.new_tournament(tournament_name=tournament, perma_id=perma_id, subject_name=subject_name)
    pass


@click.command()
@click.option("--tournament", "-t", type=click.Choice(helpers.tournament_names()))
@click.option("--year", "-y", type=int)
def new_event(tournament, year):
    """
    """
    command.new_event(tournament=helpers.to_tournament(tournament), year=year)
    pass


@click.command()
@click.option("--tournament", "-t", type=click.Choice(helpers.tournament_names()))
@click.option("--year", "-y", type=int)
def add_entries(tournament, year):
    """
    """
    command.add_entries(tournament=helpers.to_tournament(tournament), year=year)
    pass


@click.command()
@click.option("--tournament", "-t", type=click.Choice(helpers.tournament_names()))
@click.option("--year", "-y", type=int)
@click.option("--for-round", "-r", type=int, default=1, help="The round number to scrap.")
def add_round_results(tournament, year, for_round):
    """
    """
    command.leaderboard_for_round(tournament=helpers.to_tournament(tournament), year=year, for_round=for_round)
    # command.leaderboard_for_round2(tournament=tournament, year=year, for_round=for_round)
    pass



cli.add_command(new_tournament)
cli.add_command(new_event)
cli.add_command(add_entries)
cli.add_command(add_round_results)
