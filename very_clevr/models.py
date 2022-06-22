"""High-level data models/components for the learner."""

import numpy as np


class ConceptTable:
    """A look-up table for concepts that have been identified."""

    def __init__(self, initial_concepts: dict = None):
        self.concepts = {}

    def __getitem__(self, key):
        #
        if key not in self.concepts:
            raise KeyError("Concept not stored")

    def __setitem__(self, key, value):
        self.concepts[key] = {value: value}

    def __contains__(self, key):
        return key in self.concepts

    @classmethod
    def from_file(file_location: str):
        # TODO: load_from_file
        return ConceptTable(initial_concepts={})

    def export(self, filename: str = None):
        if filename is None:
            filename = "concept_table"  # TODO: Generate from date
        result = ""
        # TODO: Serialize contents to files

    def __str__(self):
        return """ConceptTable()"""


class ConceptEmbedding(np.ndarray):
    def __new__(
        subtype,
        shape,
        dtype=float,
        buffer=None,
        offset=0,
        strides=None,
        order=None,
        info=None,
    ):
        # Create the ndarray instance of our type, given the usual
        # ndarray input arguments.  This will call the standard
        # ndarray constructor, but return an object of our type.
        # It also triggers a call to InfoArray.__array_finalize__
        obj = super().__new__(subtype, shape, dtype, buffer, offset, strides, order)
        # set the new 'info' attribute to the value passed
        obj.info = info
        # Finally, we must return the newly created object:
        return obj

    def __array_finalize__(self, obj):
        # ``self`` is a new object resulting from
        # ndarray.__new__(InfoArray, ...), therefore it only has
        # attributes that the ndarray.__new__ constructor gave it -
        # i.e. those of a standard ndarray.
        #
        # We could have got to the ndarray.__new__ call in 3 ways:
        # From an explicit constructor - e.g. InfoArray():
        #    obj is None
        #    (we're in the middle of the InfoArray.__new__
        #    constructor, and self.info will be set when we return to
        #    InfoArray.__new__)
        if obj is None:
            return
        # From view casting - e.g arr.view(InfoArray):
        #    obj is arr
        #    (type(obj) can be InfoArray)
        # From new-from-template - e.g infoarr[:3]
        #    type(obj) is InfoArray
        #
        # Note that it is here, rather than in the __new__ method,
        # that we set the default value for 'info', because this
        # method sees all creation of default objects - with the
        # InfoArray.__new__ constructor, but also with
        # arr.view(InfoArray).
        self.info = getattr(obj, "info", None)
        # We do not need to return anything


class Concept:
    """A human-understandable concept"""

    def __init__(self, embedding: ConceptEmbedding):
        self._embedding = embedding
        self._name = ""

    @property
    def name(self):
        return self._name

    def __str__(self):
        return


class SymbolTape:
    """

    What the heck even is "symbolic differentiation"?

    I suppose the analogy here is that this tape automatically performs
    deductive reasoning by queuing operations

    Efficiently executes programs in a step-wise fashion

    This is the thing that performs operations on variables.

    As soon as this tape exits, its memory is cleared.

    This takes some inspiration from TensorFlow's GradientTape.

    ```
    variable = Concept()

    with SymbolTape() as t:
        t.watch(variable)
    ```
    """

    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, typ, value, traceback):
        pass

    def reset(self):
        """Clear all data stored in this tape."""

    def pop(self):
        pass

    def push(self, arg):
        pass


class Operation:
    """A discrete operation in a neurosymbolic(?) program."""


class Program:
    """Does something with an instance"""

    def __init__(self):
        self.operation = Operation()
        self.data = ...


class FeatureModule:
    """Extracts features.

    This is primarily used for entity instance identification in downstream tasks."""


class ConceptLearner:
    """Creates variables"""

    def learn(self, data):
        features = self._extract_features(data)

    def _extract_features(self, data):
        pass


class ReasoningModule:
    """Applies variable bindings to instances."""

    def reason(self):
        with SymbolTape() as t:
            pass


class InferenceEngine:
    """Extrapolates based on rules"""

    def __init__(self, concepts: ConceptTable):
        pass

    def infer(self):
        """"""

    def execute_program(self, program: Program):
        pass
