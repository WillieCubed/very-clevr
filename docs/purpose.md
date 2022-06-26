# Purpose

Very CLEVR is a model that learns explicit, composable concepts from grounded
data.

## Goals

- Create a query-able table of concepts
- Represent entities as composable building blocks of other entities
- Perform reasoning when given objects to identify

# Brainstorming

General plan:

- Use NN to extract features
- Create look-up table of features based on queries
- Map features to concepts
- Evaluate based on exemplars for specific concepts

# Other People's Ideas

- Relation Networks
  - https://arxiv.org/abs/1706.01427
- NSCL and variants
  - https://arxiv.org/abs/1904.12584
- Prototypical Contrastive Learning of Unsupervised Representations
  - https://arxiv.org/abs/2005.04966