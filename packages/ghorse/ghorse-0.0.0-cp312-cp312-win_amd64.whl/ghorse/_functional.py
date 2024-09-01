"""ghorse._phorse.functional: Functional interface for ghorse."""

from ghorse._ghorse import Graph


def number_of_nodes(graph: Graph) -> int:
    # TODO: docstring
    return graph.number_of_nodes()
