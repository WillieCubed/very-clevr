"""The primary entrypoint for training the Very CLEVR system."""

from very_clevr.data import load_dataset
from very_clevr.utils.defaults import DEFAULT_DATA_LOAD_DIR, DEFAULT_DATASET_NAME


def start_training(data_dir=DEFAULT_DATA_LOAD_DIR, dataset=DEFAULT_DATASET_NAME):
    data = load_dataset(location=data_dir, name=dataset)
    # Learn concepts
    # Prepare for reasoning
    pass
