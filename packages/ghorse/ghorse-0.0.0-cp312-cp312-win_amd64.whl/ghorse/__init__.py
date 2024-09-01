"""ghorse: Python graph C extension."""

__all__ = [
    # functions
    "freeze",
    "number_of_nodes",
    # classes
    "Graph",
]

from ghorse._ghorse import Graph, freeze
from ghorse._functional import number_of_nodes
