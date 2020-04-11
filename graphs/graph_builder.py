from typing import Dict, Iterable, Hashable

from graphs.data_structures.graphs import BaseGraph
from graphs.data_structures.basic_structures import Node, Link
from graphs.exceptions import InvalidDictionaryException


class GraphBuilder:
    @classmethod
    def from_graph_dictionary(
        cls, graph_dictionary: Dict[Hashable, Iterable[Hashable]], is_directed: bool
    ) -> BaseGraph:
        cls._validate_graph_dict(graph_dictionary)
        nodes = {node: Node(node) for node in graph_dictionary.keys()}
        all_links = []
        for node, links in graph_dictionary.items():
            all_links += [
                Link(nodes[node], nodes[link_node], is_directed) for link_node in links
            ]
        return BaseGraph(list(nodes.values()), all_links)

    @staticmethod
    def _validate_graph_dict(graph_dict: Dict[Hashable, Iterable[Hashable]]):
        allowed_nodes = set(graph_dict.keys())
        for links in graph_dict.values():
            if not set(links).issubset(allowed_nodes):
                extra_links = set(links) - allowed_nodes
                raise InvalidDictionaryException(
                    f"Found node(s) in dictionary values that is not present in the keys: {extra_links} "
                )
