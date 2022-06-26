from time import sleep
from typing import TypeVar
import torch
import torch.nn.functional as F
from tqdm import tqdm
from very_clevr.data.preprocessing import tokenize_query

from very_clevr.models import ConceptTable, Query
from very_clevr.modules.reasoning import QueryParser
from very_clevr.modules.vision import VisualNeuralExtractorModel
from very_clevr.utils.log import logger


def process_query(query: Query):
    """Convert the query into a sequence of tokens for performing reasoning."""
    return tokenize_query(query)


class SystemState:
    """Meta training loop checkpoint.

    This records the more minute details of the system.
    """

    def __init__(self) -> None:
        self._step = 0

    def __eq__(self, other: "SystemState") -> bool:
        # TODO: Compare state values
        return super().__eq__(other)

    def __str__(self) -> str:
        """Return a human-readable form of the current state"""
        return f"SystemState={{ \
            objective={{}} \
            step={{{self._step}}} \
        }}"

    def update_step(self, step, *args):
        self._step = step

    @classmethod
    def from_file(self, filename: str) -> "SystemState":
        # TODO: Serialize system state
        return SystemState()


class VeryClevrSystem:
    def __init__(self, initial_state: SystemState = None) -> None:
        if initial_state is not None:
            self._state = initial_state
        else:
            self._state = SystemState()

        self._neural_extractor = VisualNeuralExtractorModel()
        self._query_parser = QueryParser()
        self._concept_table = ConceptTable()

    @property
    def state(self):
        return self._state

    @classmethod
    def from_state(cls, state_file: str) -> "VeryClevrSystem":
        """Initialize a new VeryClevrSystem with the given state checkpoint."""
        state = SystemState.from_file(state_file)
        return VeryClevrSystem(state)

    def learn(self, data, cycles=8):
        self._neural_extractor.train()
        self._query_parser.train()

        feature_learning_rate = 1e-3
        feature_weight_decay = 1e-4

        # TODO: Incorporate RL for concept learning
        step = 0
        reward = 0

        progress_bar = tqdm(range(cycles))
        for index, cycle in enumerate(progress_bar):
            logger.debug(f"\nStarting cycle {cycle}")
            optimizer = torch.optim.Adam(
                self._neural_extractor.parameters(),
                lr=feature_learning_rate,
                weight_decay=feature_weight_decay,
            )
            optimizer.zero_grad()
            for sample in data:
                image = sample['image']
                question = sample['question']
                logger.debug(f"Using sample: {question}")
                self._perform_training_cycle(image, optimizer)

    def _perform_training_cycle(self, data, optimizer):
        """Find best representations of data."""

        # Extract features

        features_output = self._neural_extractor(data)

        # TODO: Define custom loss function
        # loss = F.nll_loss(features_output)
        # loss.backward()

        optimizer.step()

    def evaluate(self, query):
        processed = process_query(query)
