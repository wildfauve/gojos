import click

from gojos import command, presenter
from . import helpers
from gojos.initialiser import environment, db


def tournament_names():
    return helpers.tournament_names()


@click.group()
def cli():
    pass


@click.command()
@click.option("--tournament", "-t", type=click.Choice(tournament_names()), help="The name of the tournament")
@click.option("--year", "-y", type=int)
@click.option("--to-discord/--to-shell", "-d/-s", required=True, default=False, help="To discord or to the shell")
def leaderboard(tournament, year, to_discord):
    """
    Starts the tournament,  applies the results, applies the fantasy selection and prints the leaderboard
    """
    presenter.event_team_scores_table(
        command.build_leaderboard(tournament=helpers.to_tournament(tournament), year=year, to_discord=to_discord),
        to_discord
    )
    pass


@click.option('--file', '-f', required=True)
@click.option("--tournament", "-t", type=click.Choice(tournament_names()), help="The name of the tournament")
@click.option("--year", "-y", type=int)
@click.option("--ranking-plot/--accum-totals-plot", "-r/-a", required=True, help="Plot Position, or plot total scores")
@click.option("--to-discord", "channel", required=False, flag_value="to-discord", default=False,
              help="Post the plot to Discord")
@click.command()
def plot(file, tournament, year, ranking_plot, channel):
    """
    Generate a Ranking Graph
    """
    command.rank_plot(file=file, tournament=helpers.to_tournament(tournament), year=year, ranking_plot=ranking_plot)
    presenter.plot_to_channel(file, channel)
    pass


@click.command()
@click.option("--tournament", "-t", type=click.Choice(tournament_names()), help="The name of the tournament")
@click.option("--year", "-y", type=int)
@click.option("--for-round", "-r", type=int, default=1, help="The round number to assess.")
@click.option("--to-discord/--to-shell", "-d/-s", required=True, default=False, help="To discord or to the shell")
def cut_danger(tournament, year, for_round, to_discord):
    """
    Starts the tournament,  applies the results, applies the fantasy selection and prints the leaderboard
    """
    presenter.cut_assessment_table(
        command.cut_danger(tournament=helpers.to_tournament(tournament),
                           year=year,
                           for_round=for_round,
                           to_discord=to_discord), to_discord)
    pass


cli.add_command(leaderboard)
cli.add_command(plot)
cli.add_command(cut_danger)
