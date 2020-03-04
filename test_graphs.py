import pytest
from graphs.graphs import Node, Link, Graph
from itertools import combinations


@pytest.fixture
def nodes():
    n1 = Node()
    n2 = Node()
    n3 = Node()
    n4 = Node()
    n5 = Node()
    return [n1, n2, n3, n4, n5]


@pytest.fixture
def line_links(nodes):
    n1, n2, n3, n4, n5 = nodes
    link1 = Link(n1, n2)
    link2 = Link(n2, n3)
    link3 = Link(n3, n4)
    link4 = Link(n4, n5)
    return [link1, link2, link3, link4]


@pytest.fixture
def line_graph(nodes, line_links):
    return Graph(nodes, line_links)


def test_line_graph(nodes, line_links, line_graph):
    assert line_graph.order == 5
    assert line_graph.size == 4

    n1, n2, n3, n4, n5 = nodes

    assert line_graph.are_neighbours(n1, n2)
    assert line_graph.are_neighbours(n3, n4)
    assert not line_graph.are_neighbours(n1, n5)
    assert not line_graph.are_neighbours(n2, n4)
    assert line_graph.get_neighbourhood(n1) == {n2}
    assert line_graph.get_neighbourhood(n2) == {n1, n3}
    assert line_graph.get_degree(n2) == 2
    assert sorted(line_graph.degree_sequence) == [1, 1, 2, 2, 2]
    assert line_graph.maximum_degree == 2
    assert line_graph.minimum_degree == 1
    assert not line_graph.is_k_regular(1)
    for i, j in combinations(nodes, 2):
        path = line_graph.get_connections(i, j)
        assert path.is_possible

    path = line_graph.get_connections(n1, n5)
    assert path.paths == [(n1, n2, n3, n4, n5)]
    assert path.distance == 4
    path = line_graph.get_connections(n2, n4)
    assert path.paths == [(n2, n3, n4)]
    assert path.distance == 2
    path = line_graph.get_connections(n5, n4)
    assert path.paths == [(n5, n4)]
    assert path.distance == 1
    for node in nodes:
        assert node in line_graph.nodes
