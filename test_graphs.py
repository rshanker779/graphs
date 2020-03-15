import pytest
from graphs.graphs import Node, Link, Graph, PathLink
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
def complete_links(nodes):
    pairs = combinations(nodes, 2)
    return [Link(i, j) for i, j in pairs]


@pytest.fixture
def disconnected_links(nodes):
    n1, n2, n3, n4, n5 = nodes
    return [Link(n1, n2), Link(n3, n4)]


@pytest.fixture
def directed_links(nodes):
    n1, n2, n3, n4, n5 = nodes
    return [
        Link(n1, n2, True),
        Link(n2, n3, True),
        Link(n1, n4, True),
        Link(n4, n5, True),
    ]


@pytest.fixture
def cyclic_directed_links(nodes):
    n1, n2, n3, n4, n5 = nodes
    return [Link(n1, n2, True), Link(n2, n3, True), Link(n3, n1, True)]


@pytest.fixture
def line_graph(nodes, line_links):
    return Graph(nodes, line_links)


@pytest.fixture
def complete_graph(nodes, complete_links):
    return Graph(nodes, complete_links)


@pytest.fixture
def disconnected_graph(nodes, disconnected_links):
    return Graph(nodes, disconnected_links)


@pytest.fixture
def directed_graph(nodes, directed_links):
    return Graph(nodes, directed_links)


@pytest.fixture
def cyclic_directed_graph(nodes, cyclic_directed_links):
    return Graph(nodes, cyclic_directed_links)


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
        path = line_graph.get_paths(i, j)
        assert path.is_possible

    path = line_graph.get_paths(n1, n5)
    assert len(path.paths) == 1
    assert path.distance == 4
    path = line_graph.get_paths(n2, n4)
    assert len(path.paths) == 1
    assert path.distance == 2
    path = line_graph.get_paths(n5, n4)
    assert len(path.paths) == 1
    assert path.distance == 1
    for node in nodes:
        assert line_graph.get_connected_component(node) == set(nodes)
        assert node in line_graph.nodes
    assert set(nodes) in line_graph.connected_components
    assert line_graph.is_connected
    assert not line_graph.is_cyclic


def test_complete_graph(complete_graph, nodes):
    assert complete_graph.order == 5
    assert complete_graph.size == 10

    for first, second in combinations(nodes, 2):
        assert complete_graph.are_neighbours(first, second)
        assert complete_graph.get_neighbourhood(first) == set(nodes) - {first}
        assert complete_graph.get_degree(first) == 4
        assert complete_graph.get_paths(first, second).is_possible
    assert set(complete_graph.degree_sequence) == {4}
    assert complete_graph.maximum_degree == 4
    assert complete_graph.minimum_degree == 4
    assert not complete_graph.is_k_regular(1)
    assert complete_graph.is_k_regular(4)

    for node in nodes:
        assert complete_graph.get_connected_component(node) == set(nodes)
        assert node in complete_graph.nodes
    assert set(nodes) in complete_graph.connected_components
    assert complete_graph.is_connected
    assert complete_graph.is_cyclic


def test_disconnected_graph(disconnected_graph, nodes):
    assert disconnected_graph.order == 5
    assert disconnected_graph.size == 2

    n1, n2, n3, n4, n5 = nodes

    assert disconnected_graph.are_neighbours(n1, n2)
    assert disconnected_graph.are_neighbours(n3, n4)
    assert not disconnected_graph.are_neighbours(n1, n4)
    assert not disconnected_graph.are_neighbours(n2, n3)
    assert disconnected_graph.get_neighbourhood(n1) == {n2}
    assert disconnected_graph.get_neighbourhood(n2) == {n1}
    assert disconnected_graph.get_degree(n2) == 1
    assert sorted(disconnected_graph.degree_sequence) == [0, 1, 1, 1, 1]
    assert disconnected_graph.maximum_degree == 1
    assert disconnected_graph.minimum_degree == 0
    assert not disconnected_graph.is_k_regular(1)
    assert disconnected_graph.get_paths(n1, n2).is_possible
    assert disconnected_graph.get_paths(n3, n4).is_possible
    assert not disconnected_graph.get_paths(n1, n3).is_possible
    assert not disconnected_graph.get_paths(n1, n4).is_possible
    assert not disconnected_graph.get_paths(n2, n3).is_possible
    assert not disconnected_graph.get_paths(n2, n4).is_possible

    path = disconnected_graph.get_paths(n1, n2)
    assert path.paths == [(PathLink(n1, n2, Link(n1, n2)),)]
    assert path.distance == 1
    path = disconnected_graph.get_paths(n2, n4)
    assert path.paths == []
    assert disconnected_graph.get_connected_component(n1) == {n1, n2}
    assert disconnected_graph.get_connected_component(n3) == {n3, n4}
    assert {n1, n2} in disconnected_graph.connected_components
    assert {n3, n4} in disconnected_graph.connected_components
    assert {n5} in disconnected_graph.connected_components
    assert not disconnected_graph.is_connected
    assert not disconnected_graph.is_cyclic


def test_directed_graph(directed_graph, nodes):

    assert directed_graph.order == 5
    assert directed_graph.size == 4

    n1, n2, n3, n4, n5 = nodes

    assert directed_graph.are_neighbours(n1, n2)
    assert not directed_graph.are_neighbours(n2, n1)
    assert directed_graph.are_neighbours(n4, n5)
    assert not directed_graph.are_neighbours(n4, n1)
    assert directed_graph.get_neighbourhood(n1) == {n2, n4}
    assert directed_graph.get_neighbourhood(n2) == {n3}
    assert directed_graph.get_degree(n1) == 2
    assert sorted(directed_graph.degree_sequence) == [0, 0, 1, 1, 2]
    assert directed_graph.maximum_degree == 2
    assert directed_graph.minimum_degree == 0
    assert directed_graph.get_paths(n1, n2).is_possible
    assert not directed_graph.get_paths(n2, n1).is_possible
    assert directed_graph.get_paths(n4, n5).is_possible
    assert not directed_graph.get_paths(n5, n4).is_possible

    path = directed_graph.get_paths(n1, n2)
    assert path.paths == [(PathLink(n1, n2, Link(n1, n2, True)),)]
    assert path.distance == 1
    path = directed_graph.get_paths(n2, n1)
    assert path.paths == []
    assert directed_graph.get_connected_component(n1) == set(nodes)
    assert directed_graph.is_connected
    assert not directed_graph.is_cyclic
    assert directed_graph.is_dag


def test_directed_acyclic_graph(nodes, cyclic_directed_graph):
    cyclic_directed_graph.plot_graph()
    assert cyclic_directed_graph.is_cyclic
    assert not cyclic_directed_graph.is_dag
