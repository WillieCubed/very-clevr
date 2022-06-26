import torch
import torch.nn as nn
import torch.nn.functional as F


class VisualNeuralExtractorModel(nn.Module):
    """A model that extracts visual features from images."""

    def __init__(self, input_size=7, out_features=16) -> None:
        super().__init__()
        self._flatten = nn.Flatten()
        self._dense = nn.Linear(input_size, out_features)

    def forward(self, x):
        # x = torch.flatten(x, 1)
        x = self._flatten(x)
        x = F.relu(self._dense(x))
        return x


# 2022-06-26
# Also see https://arxiv.org/abs/2005.04966
#
# For image feature learning, we could do some contrastive learning
# so that we're "contrasting" a known exemplar (or prototype) of some feature
# group

# N-exemplars learning:
# - Start with existing exemplars
# - When presented with a new data input, attempt to find associations
#   with existing exemplars
# -
# Dense Prototype Learning
# - Learn a single representation of a concept
#
# TODO: Test n_exemplars learning vs dense prototype learning
# Multiple exemplars may allow for more rapid learning of new concepts
# It may be easier to learn concepts by finding counter-exemplars.
# e.g. when presented with a new set of features that can be used to
# classify an existint concept, we find the likelihood
# that it doesn't match an exemplar for another concept.
