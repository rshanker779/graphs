from typing import List, Set, Iterable, Tuple
import matplotlib.pyplot as plt
import numpy as np
import pytest

from mixin import StringMixin


class Node(StringMixin):
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


class PathReport:
    def __init__(self, from_node: Node, to_node: Node, paths: List[Tuple[Node, ...]]):
        self.from_node = from_node
        self.to_node = to_node
        self.is_possible = len(paths) > 0
        self.paths = paths
        self.distance = min(len(p) for p in paths) - 1 if paths else -1


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

    def get_connections(self, node_1: Node, node_2: Node) -> PathReport:

        paths = [(node_1,)]
        # We traverse breadth first to expand to all possible (acyclic) paths visiting unique points
        # Note if we have Link(1,2) and Link(2,1), we would still only get the path 1,2.
        # This is more about connectivity then full path enumeration
        while True:
            next_paths = paths
            for *initial, p in paths:
                next_steps = self.get_neighbourhood(p) - set(initial)
                next_paths += [tuple([*initial, p, i]) for i in next_steps]
            if len(next_paths) == len(paths):
                paths = next_paths
                break
            paths = next_paths
            print(paths)
        paths_between = [i for i in paths if i[-1] == node_2]
        return PathReport(node_1, node_2, paths_between)

    def get_connected_component(self, node: Node) -> Set[Node]:

        neighbourhood = self.get_neighbourhood(node) | {node}
        processed_nodes = {node}
        while neighbourhood != set(processed_nodes):
            next_node = next(i for i in neighbourhood - processed_nodes)
            neighbourhood |= self.get_neighbourhood(next_node)
            processed_nodes |= {next_node}
        return neighbourhood

    @property
    def connected_components(self) -> List[Set[Node]]:
        processed_nodes = set()
        components = []
        while processed_nodes != self.nodes:
            next_node = next(i for i in self.nodes - processed_nodes)
            component = self.get_connected_component(next_node)
            components.append(component)
            processed_nodes |= component
        return components

    @property
    def is_connected(self):
        return len(self.connected_components) == 1
