import click

from gojos import command, presenter
from gojos.majors import tournaments

from gojos.initialiser import environment

def tournament_names():
    return tournaments.tournament_names()


@click.group()
def cli():
    pass

@click.command()
@click.option("--tournament", "-t",
              type=click.Choice(tournament_names()),
              help="The name of the tournament")
@click.option("--to-discord/--to-shell", "-d/-s", required=True, default=False, help="To discord or to the shell")
def leaderboard(tournament, to_discord):
    """
    Starts the tournament,  applies the results, applies the fantasy selection and prints the leaderboard
    """
    presenter.event_team_scores_table(
        command.leaderboard_df(tournament),
        to_discord
    )
    pass



@click.command()
@click.option("--entries-file", "-e", type=str, default=None, help="Entries File")
@click.option("--players-file", "-p", type=str, default=None, help="Players File")
@click.option("--leaderboard-file", "-l", type=str, default=None, help="Leaderboard File")
@click.option("--for-round", "-r", type=int, default=1, help="The round number to scrap.")
def leaderboard_scrap(entries_file, players_file, leaderboard_file, for_round):
    """
    """
    command.leaderboard_scrap(entries_file=entries_file,
                              players_file=players_file,
                              leaderboard_file=leaderboard_file,
                              for_round=for_round)
    pass


@click.option('--file', '-f', required=True)
@click.option("--tournament", "-t",
              type=click.Choice(tournament_names()),
              help="The name of the tournament")
@click.option("--ranking-plot/--accum-totals-plot", "-r/-a", required=True, help="Plot Position, or plot total scores")
@click.option("--to-discord", "channel", required=False, flag_value="to-discord", default=False,
              help="Post the plot to Discord")
@click.command()
def plot(file, tournament, ranking_plot, channel):
    """
    Generate a Ranking Graph
    """
    command.rank_plot(file=file, tournament_name=tournament, ranking_plot=ranking_plot)
    presenter.plot_to_channel(file, channel)
    pass


@click.command()
@click.option("--tournament", "-t",
              type=click.Choice(tournament_names()),
              help="The name of the tournament")
@click.option("--to-discord/--to-shell", "-d/-s", required=True, default=False, help="To discord or to the shell")
def cut_danger(tournament, to_discord):
    """
    Starts the tournament,  applies the results, applies the fantasy selection and prints the leaderboard
    """
    presenter.cut_assessment_table(
        command.cut_danger(tournament),
        to_discord
    )
    pass



cli.add_command(leaderboard)
cli.add_command(plot)
cli.add_command(leaderboard_scrap)
cli.add_command(cut_danger)
