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
        """Start the Very CLEVR live demo.

        This will start a web-based live demo of the Very CLEVR system using
        Gradio. The URL of the demo can be found in the standard output.
        """
        launch_interactive_demo()


def run_cli():
    """Start the Very CLEVR command line interface."""
    fire.Fire(VeryClevrCLI)
