from ghorse import Graph

def test_init():
    graph = Graph()
    assert graph.number_of_nodes() == 0
