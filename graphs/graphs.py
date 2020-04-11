import operator
from functools import reduce
from typing import Dict, Iterable, Hashable
from typing import List, Set, Tuple, Optional, FrozenSet

import matplotlib.pyplot as plt
from more_itertools import flatten

from graphs.data_structures.basic_structures import Node, Link
from graphs.data_structures.graphs import BaseGraph
from graphs.data_structures.paths import PathLink, PathReport
from graphs.graph_builder import GraphBuilder
from graphs.graph_properties import (
    NeighbouringGraphProperties,
    DegreeProperties,
    DirectedAcyclicGraphProperties,
)
from graphs.plots import GraphPlotter


class Graph(BaseGraph):
    @classmethod
    def from_base_graph(cls, graph: BaseGraph):
        return cls(graph.nodes, graph.links)

    @classmethod
    def from_graph_dictionary(
        cls, graph_dictionary: Dict[Hashable, Iterable[Hashable]], is_directed: bool
    ):
        base_graph = GraphBuilder.from_graph_dictionary(graph_dictionary, is_directed)
        return cls.from_base_graph(base_graph)

    def __init__(self, nodes: List[Node], links: List[Link]):
        super().__init__(nodes, links)
        self.neighbouring_graph_properties = NeighbouringGraphProperties(self)
        self.plotter = GraphPlotter(self)
        self.degree_properties = DegreeProperties(self)
        self.dag_properties = DirectedAcyclicGraphProperties(self)

    def plot_graph(self) -> plt.Figure:
        return self.plotter.plot_graph()

    @property
    def order(self) -> int:
        return len(self.nodes)

    @property
    def size(self) -> int:
        return len(self.links)

    def find_link(self, node_1, node_2) -> Optional[Link]:
        return self.neighbouring_graph_properties.find_link(node_1, node_2)

    def is_in_graph(self, node: Node) -> bool:
        return self.neighbouring_graph_properties.is_in_graph(node)

    def are_neighbours(self, node_1: Node, node_2: Node) -> bool:
        return self.neighbouring_graph_properties.are_neighbours(node_1, node_2)

    def get_neighbourhood(self, node: Node) -> Set[Node]:
        return self.neighbouring_graph_properties.get_neighbourhood(node)

    def get_degree(self, node: Node) -> int:
        return self.degree_properties.get_degree(node)

    @property
    def degree_sequence(self) -> List[int]:
        return self.degree_properties.degree_sequence

    @property
    def maximum_degree(self) -> int:
        return self.degree_properties.maximum_degree

    @property
    def minimum_degree(self) -> int:
        return self.degree_properties.minimum_degree

    def is_k_regular(self, k: int) -> bool:
        return self.degree_properties.is_k_regular(k)

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

    @property
    def dependency_chain(self):
        if self.is_dag:
            return self.dag_properties.dependency_chain
        return []
