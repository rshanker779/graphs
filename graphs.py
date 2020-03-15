import operator
from functools import reduce
from typing import List, Set, Iterable, Tuple, Optional, FrozenSet
import matplotlib.pyplot as plt
import numpy as np
import pytest
from more_itertools import flatten

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


class Link(StringMixin):
    def __init__(self, node_1: Node, node_2: Node, is_directed: bool = False):
        super().__init__()
        self.node_1 = node_1
        self.node_2 = node_2
        self.is_directed = is_directed

    def __hash__(self):
        return hash((self.node_1, self.node_2, self.is_directed))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (self.node_1, self.node_2, self.is_directed) == (
            other.node_1,
            other.node_2,
            other.is_directed,
        )

    @property
    def nodes(self) -> List[Node]:
        return [self.node_1, self.node_2]


class PathLink(Link):
    def __init__(self, node_1, node_2, underlying_link):
        super().__init__(node_1, node_2, True)
        self.underlying_link = underlying_link


class PathReport:
    def __init__(
        self, from_node: Node, to_node: Node, paths: List[Tuple[PathLink, ...]]
    ):
        self.from_node = from_node
        self.to_node = to_node
        self.is_possible = len(paths) > 0
        self.paths = paths
        self.distance = min(len(p) for p in paths) if paths else -1


class Graph:
    def __init__(self, nodes: List[Node], links: List[Link]):
        self.nodes = set(nodes)
        assert all(i.is_directed for i in links) or all(
            not i.is_directed for i in links
        )
        self.is_directed = next(i.is_directed for i in links)
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
            x = [np.real(i) for i in points]
            y = [np.imag(i) for i in points]
            plt.plot(x, y, c="b")
            if link.is_directed:
                eps = 0.02
                plt.arrow(
                    x[-1],
                    y[-1],
                    eps * (x[-1] - x[0]),
                    eps * (y[-1] - y[0]),
                    shape="full",
                    lw=0,
                    length_includes_head=True,
                    head_width=0.05,
                )
        plt.show()

    @property
    def order(self) -> int:
        return len(self.nodes)

    @property
    def size(self) -> int:
        return len(self.links)

    def find_link(self, node_1, node_2) -> Optional[Link]:
        forward_link = Link(node_1, node_2, self.is_directed)
        if forward_link in self.links:
            return forward_link
        backwards_link = Link(node_2, node_1)
        if backwards_link in self.links:
            return backwards_link

    def get_roots_of_unity(self, k, n) -> complex:
        return np.exp(2 * np.pi * 1j * k / n)

    def is_in_graph(self, node: Node) -> bool:
        return node in self.nodes

    def are_neighbours(self, node_1: Node, node_2: Node) -> bool:
        """Returns if there is a length one path between node_1 and node_2"""
        return self.find_link(node_1, node_2) is not None

    def get_neighbourhood(self, node: Node) -> Set[Node]:
        matching_links = [
            self.find_link(node, n)
            for n in self.nodes
            if self.find_link(node, n) is not None
        ]
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

    def get_paths(self, node_1: Node, node_2: Node) -> PathReport:

        paths: List[Tuple[PathLink, ...]] = []
        for node in self.get_neighbourhood(node_1):
            link = self.find_link(node_1, node)
            if link is not None:
                paths.append((PathLink(node_1, node, link),))
        # We traverse breadth first to expand to all possible (acyclic) paths visiting unique points
        # Note if we have Link(1,2) and Link(2,1), we would still only get the path 1,2.
        # This is more about connectivity then full path enumeration
        while True:
            next_paths = paths
            for *initial, last_link in paths:
                last_node = last_link.node_2
                next_steps = self.get_neighbourhood(last_node) - set(
                    flatten(i.nodes for i in initial)
                )
                for step in next_steps:
                    link = self.find_link(last_node, step)
                    if (
                        link is not None
                        and link not in {i.underlying_link for i in initial}
                        and link != last_link.underlying_link
                    ):
                        next_paths.append(
                            tuple(
                                [*initial, last_link, PathLink(last_node, step, link)]
                            )
                        )
            if len(next_paths) == len(paths):
                paths = next_paths
                break
            paths = next_paths
            print(paths)
        paths_between = [i for i in paths if i[-1].node_2 == node_2]
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
    def connected_components(self) -> Set[FrozenSet[Node]]:
        processed_nodes = set()
        components = set()
        while processed_nodes != self.nodes:
            next_node = next(i for i in self.nodes - processed_nodes)
            component = self.get_connected_component(next_node)
            components.add(frozenset(component))
            processed_nodes |= component
        if not self.is_directed:
            return components

        clean_components = set()
        while True:
            previous_length = len(clean_components)
            for node in self.nodes:
                nodes_components = reduce(
                    operator.or_, [i for i in components if node in i], frozenset()
                )
                clean_components.add(nodes_components)
            if len(clean_components) != previous_length:
                break
        return clean_components

    @property
    def is_connected(self):
        return len(self.connected_components) == 1

    @property
    def is_cyclic(self):
        for starting_node in self.nodes:
            for next_node in self.nodes - {starting_node}:
                connections = self.get_paths(starting_node, next_node)
                for path in connections.paths:
                    last_link = path[-1]
                    underlying_links = {i.underlying_link for i in path}
                    next_link = self.find_link(last_link.node_2, starting_node)
                    if next_link is not None and next_link not in underlying_links:
                        return True
        return False

    @property
    def is_dag(self):
        return self.is_directed and not self.is_cyclic

    @property
    def is_eulerian(self):
        return all(self.get_degree(node) % 2 == 0 for node in self.nodes)
