from itertools import combinations

import pytest

from graphs.data_structures.basic_structures import Node, Link
from graphs import Graph


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
