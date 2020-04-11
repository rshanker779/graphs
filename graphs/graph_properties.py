from typing import Set, List

from graphs.data_structures.basic_structures import Node, Link
from graphs.data_structures.graphs import BaseGraph


class BaseGraphProperties:
    def __init__(self, graph: BaseGraph):
        self.graph = graph
        self.links = self.graph.links
        self.nodes = self.graph.nodes
        self.is_directed = self.graph.is_directed


class NeighbouringGraphProperties(BaseGraphProperties):
    def find_link(self, node_1: Node, node_2: Node):
        forward_link = Link(node_1, node_2, self.is_directed)
        if forward_link in self.links:
            return forward_link
        backwards_link = Link(node_2, node_1)
        if backwards_link in self.links:
            return backwards_link

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


class DegreeProperties(BaseGraphProperties):
    def __init__(self, graph: BaseGraph):
        super().__init__(graph)
        self.neighbouring_graph_properties = NeighbouringGraphProperties(graph)

    def get_degree(self, node: Node) -> int:
        return len(self.neighbouring_graph_properties.get_neighbourhood(node))

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


class DirectedAcyclicGraphProperties(BaseGraphProperties):
    def __init__(self, graph: BaseGraph):
        super().__init__(graph)
        self.neighbouring_graph_properties = NeighbouringGraphProperties(graph)

    @property
    def dependency_chain(self) -> List[Node]:
        chain = []
        processed_nodes = set()
        while processed_nodes != self.nodes:
            for node in self.nodes - processed_nodes:
                neighbourhood = self.neighbouring_graph_properties.get_neighbourhood(
                    node
                )
                if not neighbourhood - processed_nodes:
                    chain.append(node)
                    processed_nodes.add(node)
        return chain
