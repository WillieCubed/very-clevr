from dataclasses import dataclass


def check_similarity():
    pass


@dataclass
class EvaluationMetric:
    name: str


def evaluate(test_data: tuple, database) -> EvaluationMetric:
    """Check to see to what degree the database matches what the given input.

    THIS IS THE MAIN THING! We want to build a database of concepts
    """
    database = ...

    similarity = check_similarity()
