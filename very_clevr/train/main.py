"""The primary entrypoint for training the Very CLEVR system."""

from very_clevr.data.clevr_dataset_connector import (
    ClevrDatasetStateDescription,
    build_dictionaries,
)
from very_clevr.system import VeryClevrSystem
from very_clevr.utils.defaults import DEFAULT_DATA_LOAD_DIR, DEFAULT_DATASET_NAME
from very_clevr.utils.log import logger


def start_training(
    data_dir=DEFAULT_DATA_LOAD_DIR, state_file: str = None, dataset=DEFAULT_DATASET_NAME
):
    if dataset != DEFAULT_DATASET_NAME:
        raise ValueError(f'Dataset "{dataset}" currently not supported.')

    # Load data
    logger.debug("Loading data")
    word_dictionary = build_dictionaries(data_dir)
    clevr_dataset_train = ClevrDatasetStateDescription(data_dir, True, word_dictionary)

    # Initialize system
    if state_file is not None:
        logger.info(f"Loading system from new state at location: {state_file}")
        system = VeryClevrSystem.from_state(state_file)
    else:
        logger.info("Loading system with new state")
        system = VeryClevrSystem()

    # Learn concepts
    logger.info("Starting training process")
    system.learn(clevr_dataset_train)

    # Prepare for reasoning

    # TODO: Learn from state
