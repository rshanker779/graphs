from typing import List, Tuple

from graphs.data_structures.basic_structures import Link, Node


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
