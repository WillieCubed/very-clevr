"""
This thing should be learning rules.

TODO:
Generalized
Battery
of
Datasets
(GBoD)
"""

from dataclasses import dataclass
import gradio as gr

import fire

from very_clevr.demo import launch_interactive_demo


class Rule:
    """
    TODO: Use knowledge of context-free grammar
    """

    def __init__(self):
        pass

    def apply(input_x) -> bool:
        """
        Return True or which rules were violated.
        """
        return True


class Model:
    def query(self):
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


def train(location="data"):
    data = load_data(location=location)


class VeryClevrCLI:
    """A CLI that exposes tools for training and testing the Very CLEVR system"""

    def train(self):
        pass

    def evaluate(self):
        pass

    def interact(self):
        launch_interactive_demo()


def run_cli():
    fire.Fire(VeryClevrCLI)


__all__ = ["run_cli"]
