from app.evaluation import (
    calculate_simple_score,
    EqualWeightStrategy,
    RelevanceFocusedStrategy
)


def test_simple_scoring():
    result = calculate_simple_score(5, 4, 3)

    assert result == 4.0


def test_equal_weight_strategy():
    strategy = EqualWeightStrategy()

    result = strategy.calculate(5, 4, 3)

    assert result == 4.0


def test_relevance_focused_strategy():
    strategy = RelevanceFocusedStrategy()

    result = strategy.calculate(5, 4, 3)

    assert result == 4.25


def test_strategies_produce_different_results():
    equal_strategy = EqualWeightStrategy()
    relevance_strategy = RelevanceFocusedStrategy()

    equal_result = equal_strategy.calculate(5, 4, 3)
    relevance_result = relevance_strategy.calculate(5, 4, 3)

    assert equal_result != relevance_result

