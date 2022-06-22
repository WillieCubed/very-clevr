import tensorflow_datasets as tfds
from typing import List

DEFAULT_DATASETS = ["clevr"]


def load_data(paths=DEFAULT_DATASETS):
    """Return the data from the given selection."""
    data = tfds.load("clevr", split="train", shuffle_files=True)


class Learner:
    pass


def train():

    # Get data

    # Create concepts

    return
