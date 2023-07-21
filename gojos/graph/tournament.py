from rdflib import Graph, RDF, URIRef, Literal

from gojos import rdf, adapter, graph


def tournament_subject(g, tournament):
    return rdf.first_match(g, (None, rdf.hasSubjectName, Literal(tournament)), form=rdf.subject)


def events_for_tournament(g, tournament):
    return rdf.all_matching(g, (None, rdf.isEventOf, tournament_subject(g, tournament)), form=rdf.subject)


def event_for_year(g, event_subs, year):
    for_year = [rdf.first_match(g, (sub, rdf.isInYear, Literal(year)), form=rdf.subject) for sub in event_subs]
    return for_year


def scrap_leaderboard(for_round):
    return adapter.build_leaderboard(for_round, False)

def player_score_sub(g, player_sub):
    return rdf.first_match(g, (None, rdf.isEventScoreForPlayer, player_sub), form=rdf.subject)

def add_round_scores(g, players_g, tournament, year, for_round):
    event_sub = event_for_year(g, events_for_tournament(g, tournament), year)
    # for ps, _, _ in rdf.all_matching(g, (None, RDF.type, rdf.PLAYER_SCORE)):
    #     plr = URIRef("/".join(ps.split("/")[:-3]))
    #     g.add((ps, rdf.isEventScoreForPlayer, plr))
    # breakpoint()

    for player_score in scrap_leaderboard(for_round):
        player_sub = graph.player_sub_by_name(players_g, player_score.get('name'))
        ps_sub = player_score_sub(g, player_sub)
        breakpoint()
