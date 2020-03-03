from typing import List, Set
import matplotlib.pyplot as plt
import numpy as np
import pytest


class Node:
    _id = 0

    def __init__(self):
        self.id = self.__class__._id
        self.__class__._id += 1

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.id == other.id


class Link:
    def __init__(self, node_1: Node, node_2: Node):
        self.node_1 = node_1
        self.node_2 = node_2

    def __hash__(self):
        return hash((self.node_1, self.node_2))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (self.node_1, self.node_2) == (other.node_1, other.node_2)


class Graph:
    def __init__(self, nodes: List[Node], links: List[Link]):
        self.nodes = set(nodes)
        self.links = set(links)

    def plot_graph(self):
        n = len(self.nodes)
        point_map = {i: j for i, j in enumerate(self.nodes)}
        node_map = {j.id: self.get_roots_of_unity(i, n) for i, j in point_map.items()}
        complex_repns = [self.get_roots_of_unity(k, n) for k in point_map]
        plt.figure()
        plt.scatter(
            [np.real(i) for i in complex_repns], [np.imag(i) for i in complex_repns]
        )
        for link in self.links:
            points = [node_map[link.node_1.id], node_map[link.node_2.id]]
            plt.plot([np.real(i) for i in points], [np.imag(i) for i in points], c="b")
        plt.show()

    @property
    def order(self) -> int:
        return len(self.nodes)

    @property
    def size(self) -> int:
        return len(self.links)

    def get_roots_of_unity(self, k, n) -> complex:
        return np.exp(2 * np.pi * 1j * k / n)

    def is_in_graph(self, node: Node) -> bool:
        return node in self.nodes

    def are_neighbours(self, node_1: Node, node_2: Node) -> bool:
        return Link(node_1, node_2) in self.links or Link(node_2, node_1) in self.links

    def get_neighbourhood(self, node: Node) -> Set[Node]:
        matching_links = {l for l in self.links if l.node_1 == node or l.node_2 == node}
        return (
            {l.node_1 for l in matching_links} | {l.node_2 for l in matching_links}
        ) - {node}

    def get_degree(self, node: Node) -> int:
        return len(self.get_neighbourhood(node))

    @property
    def degree_sequence(self) -> List[int]:
        return [self.get_degree(n) for n in self.nodes]

    @property
    def maximum_degree(self) -> int:
        return max(self.get_degree(n) for n in self.nodes)

    @property
    def minimum_degree(self) -> int:
        return min(self.get_degree(n) for n in self.nodes)

    def is_k_regular(self, k: int) -> bool:
        return set(self.degree_sequence) == {k}


@pytest.fixture
def nodes():
    n1 = Node()
    n2 = Node()
    n3 = Node()
    n4 = Node()
    n5 = Node()
    return [n1, n2, n3, n4, n5]


@pytest.fixture
def links(nodes):
    n1, n2, n3, n4, n5 = nodes
    link1 = Link(n1, n2)
    link2 = Link(n2, n3)
    link3 = Link(n3, n4)
    link4 = Link(n4, n5)
    return [link1, link2, link3, link4]


@pytest.fixture
def graph(nodes, links):
    return Graph(nodes, links)


def test_graph(nodes, links, graph):
    assert graph.order == 5
    assert graph.size == 4

    n1, n2, n3, n4, n5 = nodes

    assert graph.are_neighbours(n1, n2)
    assert graph.are_neighbours(n3, n4)
    assert not graph.are_neighbours(n1, n5)
    assert not graph.are_neighbours(n2, n4)
    assert graph.get_neighbourhood(n1) == {n2}
    assert graph.get_neighbourhood(n2) == {n1, n3}
    assert graph.get_degree(n2) == 2
    assert sorted(graph.degree_sequence) == [1, 1, 2, 2, 2]
    assert graph.maximum_degree == 2
    assert graph.minimum_degree == 1
    assert not graph.is_k_regular(1)
    for node in nodes:
        assert node in graph.nodes


# if __name__ == '__main__':
#
#     link1=Link(n1, n2)
#     link2=Link(n2, n3)
#     link3=Link(n3, n4)
#     link4=Link(n4, n5)
#
#     g = Graph([n1, n2, n3, n4, n5], [link1, link2, link3, link4])
# g.plot_graph()
