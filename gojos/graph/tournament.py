from typing import NamedTuple
from functools import partial, reduce
from rdflib import Graph, RDF, URIRef, Literal

from gojos import rdf, adapter, graph
from gojos.util import fn

RoundScore = NamedTuple('RoundScore', [('round_number', int),
                                       ('score', int),
                                       ("position", int),
                                       ('running_total', int),
                                       ('state', str),
                                       ('round_subject', URIRef)])
PlayerScore = NamedTuple('PlayerScore', [('subject', URIRef),
                                         ('total', int),
                                         ('position', int),
                                         ('state', str),
                                         ('round_scores', RoundScore)])


def tournament_subject(g, tournament):
    return rdf.first_match(g, (None, rdf.hasSubjectName, Literal(tournament)), form=rdf.subject)


def events_for_tournament(g, tournament):
    return rdf.all_matching(g, (None, rdf.isEventOf, tournament_subject(g, tournament)), form=rdf.subject)


def event_for_year(g, event_subs, year):
    for_year = [rdf.first_match(g, (sub, rdf.isInYear, Literal(year)), form=rdf.subject) for sub in event_subs]
    return for_year[0]


def scrap_leaderboard(for_round):
    return adapter.build_leaderboard(for_round, False)


def player_score_sub(g, player_sub):
    return rdf.first_match(g, (None, rdf.isEventScoreForPlayer, player_sub), form=rdf.subject)


def leaderboard_sub(g, event_sub):
    return rdf.first_match(g, (None, rdf.isForEvent, event_sub), form=rdf.subject)

def leaderboard_sub_round(leaderboard_sub, for_round):
    return leaderboard_sub + f"/Round/{for_round}"

def current_player_score(g, sub):
    triples = rdf.all_matching(g, (sub, None, None))
    total = rdf.triple_finder(rdf.hasScoreTotal, triples)
    pos = rdf.triple_finder(rdf.isInCurrentPosition, triples)
    state = rdf.triple_finder(rdf.playerIsInState, triples)
    rd_scores = reduce(partial(ps_rd_bnodes, g),
                       rdf.triple_finder(rdf.hasRoundScores, triples, filter_fn=fn.select, builder=rdf.all_objects), {})
    # rd_scores = [ps_rd_bnodes(g, bn) for bn in
    #              rdf.triple_finder(rdf.hasRoundScores, triples, filter_fn=fn.select, builder=rdf.all_objects)]
    return PlayerScore(sub,
                       total.toPython(),
                       pos.toPython(),
                       state.toPython() if state else None,
                       rd_scores)


def ps_rd_bnodes(g, accum, bn_sub):
    """
    [ clo-go:hasPositionAfterRound 3 ;
        clo-go:hasRoundScore 69 ;
        clo-go:hasRunningScoreTotal 137 ;
        clo-go:isRoundNumber 2 ;
        clo-go:isRoundSubject <https://clojos.io/ontology/FantasyGolf/Ind/Tournament/ClojosOpen/2023/Leaderboard/Round/2> ]
    :param bn_sub:
    :return:
    """
    triples = rdf.all_matching(g, (bn_sub, None, None))
    rd_num = rdf.triple_finder(rdf.isRoundNumber, triples)
    pos = rdf.triple_finder(rdf.hasPositionAfterRound, triples)
    score = rdf.triple_finder(rdf.hasRoundScore, triples)
    running_total = rdf.triple_finder(rdf.hasRunningScoreTotal, triples)
    rd_sub = rdf.triple_finder(rdf.isRoundSubject, triples)
    state = rdf.triple_finder(rdf.playerIsInState, triples)
    accum[rd_num.toPython()] = RoundScore(rd_num.toPython(),
                                          score.toPython(),
                                          pos.toPython(),
                                          running_total.toPython(),
                                          state.toPython() if state else None,
                                          rd_sub)
    return accum


def add_this_round(current_state, player_score, for_round, round_sub):
    rd_score = int(player_score['round_scores']['this'])
    state = player_score['player_state']
    total = current_state.total + rd_score
    ps = RoundScore(for_round,
                    rd_score,
                    None,
                    total,
                    state,
                    round_sub)
    return PlayerScore(current_state.subject,
                       total,
                       current_state.position,
                       state,
                       round_scores={**current_state.round_scores, **{for_round: ps}})


def add_round_scores(g, players_g, tournament, year, for_round):
    event_sub = event_for_year(g, events_for_tournament(g, tournament), year)
    leaderboard = leaderboard_sub(g, event_sub)
    round_sub = leaderboard_sub_round(leaderboard, for_round)
    # for ps, _, _ in rdf.all_matching(g, (None, RDF.type, rdf.PLAYER_SCORE)):
    #     plr = URIRef("/".join(ps.split("/")[:-3]))
    #     g.add((ps, rdf.isEventScoreForPlayer, plr))
    # breakpoint()

    for player_score in scrap_leaderboard(for_round):
        player_sub = graph.player_sub_by_name(players_g, player_score.get('name'))
        new_state = add_this_round(current_player_score(g, player_score_sub(g, player_sub)),
                                   player_score,
                                   for_round,
                                   round_sub)
        breakpoint()
