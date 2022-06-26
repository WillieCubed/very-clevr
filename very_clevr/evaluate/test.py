from very_clevr.data.clevr_dataset_connector import (
    ClevrDatasetStateDescription,
    build_dictionaries,
)


def perform_inference(image_path: str, query: str):
    """Perform inference on a single instance for a model."""
    return {}


def test_batch(data_dir: str):
    word_dictionary = build_dictionaries(data_dir)
    clevr_dataset_test = ClevrDatasetStateDescription(data_dir, False, word_dictionary)
    # TODO: Actually evaluate and return batch
    return []
