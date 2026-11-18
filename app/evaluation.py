from abc import ABC, abstractmethod


# Simple approach: calculate the average directly.
def calculate_simple_score(relevance, clarity, completeness):
    scores = [relevance, clarity, completeness]
    return sum(scores) / len(scores)


# Strategy Pattern: define a common scoring interface.
class EvaluationStrategy(ABC):

    @abstractmethod
    def calculate(self, relevance, clarity, completeness):
        pass


# Strategy 1: Give all three criteria equal importance.
class EqualWeightStrategy(EvaluationStrategy):

    def calculate(self, relevance, clarity, completeness):
        return calculate_simple_score(
            relevance,
            clarity,
            completeness
        )


# Strategy 2: Give relevance more importance.
class RelevanceFocusedStrategy(EvaluationStrategy):

    def calculate(self, relevance, clarity, completeness):
        return (
            relevance * 0.50
            + clarity * 0.25
            + completeness * 0.25
        )
