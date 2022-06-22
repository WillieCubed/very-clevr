"""Utilities for Very CLEVR command line tools."""

import fire

from very_clevr.app.demo import launch_interactive_demo
from very_clevr.train.main import start_training
from very_clevr.utils.defaults import DEFAULT_DATA_LOAD_DIR, DEFAULT_DATASET_NAME


class VeryClevrCLI:
    """A CLI that exposes tools for training and testing the Very CLEVR system"""

    def train(self, data_dir=DEFAULT_DATA_LOAD_DIR, dataset_name=DEFAULT_DATASET_NAME):
        """Start training with the given parameters."""
        start_training(data_dir=data_dir, dataset=dataset_name)

    def evaluate(self, in_filename="test_inputs", out_filename="test_results.json"):
        """Perform inference on the given data.

        Args:
            test_inputs (str): The file containing
            out_filename (str): test_results.json by default.
        """
        # TODO

    def interact(self):
        """Start the Very CLEVR live demo.

        This will start a web-based live demo of the Very CLEVR system using
        Gradio. The URL of the demo can be found in the standard output.
        """
        launch_interactive_demo()


def run_cli():
    """Start the Very CLEVR command line interface."""
    fire.Fire(VeryClevrCLI)
