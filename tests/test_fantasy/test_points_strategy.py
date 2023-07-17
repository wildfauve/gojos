from rdflib import URIRef

from gojos.fantasy import points_strategy


def test_strategy_to_subject():
    strategy = points_strategy.strategy_inverted_position_1_wc_4_max_players_10()
    sub = strategy.subject()

    assert sub.toPython() == 'https://clojos.io/ontology/Fantasy/FantasyPointsStrategy/InvertedPosition/Points1_4_10'


def test_strategy_from_subject():
    sub = URIRef(
        'https://clojos.io/ontology/Fantasy/FantasyPointsStrategy/InvertedPosition/Points1_4_10')

    strategy = points_strategy.PointsStrategyCalculator.build(sub)

    assert strategy.subject() == sub


def test_strategy_from_components():
    expected_sub = URIRef(
        'https://clojos.io/ontology/Fantasy/FantasyPointsStrategy/InvertedPosition/Points1_4_10')

    strategy = points_strategy.PointsStrategyCalculator.build(
        ("InvertedPosition", "Points1_4_10"))

    assert strategy.subject() == expected_sub
