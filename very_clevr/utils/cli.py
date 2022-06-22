"""Utilities for Very CLEVR command line tools."""

import fire

from very_clevr.app.demo import launch_interactive_demo


class VeryClevrCLI:
    """A CLI that exposes tools for training and testing the Very CLEVR system"""

    def train(self):
        pass

    def evaluate(self):
        pass

    def interact(self):
        launch_interactive_demo()


def run_cli():
    """Start the Very CLEVR command line interface."""
    fire.Fire(VeryClevrCLI)
