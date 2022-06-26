"""Utilities for Very CLEVR command line tools."""

import sys
import fire

from very_clevr.app.demo import launch_interactive_demo
from very_clevr.evaluate.test import perform_inference, test_batch
from very_clevr.utils.defaults import DEFAULT_DATA_LOAD_DIR, DEFAULT_DATASET_NAME
from very_clevr.utils.io import write_to_file
from very_clevr.utils.log import logger, enable_verbose_logger
from very_clevr.train.main import start_training


class VeryClevrCLI:
    """A CLI that exposes tools for training and testing the Very CLEVR system"""

    def __init__(self, verbose=False) -> None:
        """
        Args:
            verbose (bool): Whether to display additional logging information
        """
        if verbose:
            enable_verbose_logger()
            logger.debug("Verbose mode enabled.")
        self._verbose = verbose

    def train(
        self, data_dir=DEFAULT_DATA_LOAD_DIR, dataset_name=DEFAULT_DATASET_NAME
    ) -> None:
        """Start training with the given parameters."""
        try:
            start_training(data_dir=data_dir, dataset=dataset_name)
        except ValueError as e:
            logger.error("Invalid value provided", e)
            sys.exit(1)

    def evaluate(self, image: str, query: str) -> str:
        """Perform inference on the given data.

        Args:
            image (str): The path to an image to evaluate
            query (str): A text prompt to query the image

        Returns:
            str: The output of the Very CLEVR system.
        """
        output = perform_inference(image, query)
        return output

    def evaluate_batch(
        self, data_dir=DEFAULT_DATA_LOAD_DIR, out_filename="test_results.json"
    ) -> None:
        """Perform inference on the given data.

        Args:
            image_dir (str): The file containing data to test/evaluate.
            out_filename (str): test_results.json by default.

        Returns:
            str: The output of the Very CLEVR system.
        """
        try:
            batch_results = test_batch(data_dir)
            write_to_file(out_filename, batch_results, output="json")
            return batch_results
        except IOError as e:
            logger.exception("Could not write results to file.", e)
            print("Could not write results to file.")
            sys.exit(1)
        except e:
            logger.exception("Unspecified error during evaluation.", e)
            print("Unspecified error during evaluation.")
            sys.exit(1)

    def interact(self) -> None:
        """Start the Very CLEVR live demo.

        This will start a web-based live demo of the Very CLEVR system using
        Gradio. The URL of the demo can be found in the standard output.
        """
        launch_interactive_demo()


def run_cli():
    """Start the Very CLEVR command line interface."""
    try:
        fire.Fire(VeryClevrCLI)
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received. Shutting down.")
        sys.exit(130)
