"""The primary entrypoint for training the Very CLEVR system."""

from very_clevr.data import load_dataset


DEFAULT_DATASET = "clevr"

DEFAULT_DATA_DIR = "data"


def start_training(data_dir=DEFAULT_DATA_DIR, dataset=DEFAULT_DATASET):
    data = load_dataset(location=data_dir)
    # Learn concepts
    # Prepare for reasoning
    pass
