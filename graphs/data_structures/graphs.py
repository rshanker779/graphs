from typing import List

from graphs.data_structures.basic_structures import Node, Link


class BaseGraph:
    def __init__(self, nodes: List[Node], links: List[Link]):
        self.nodes = set(nodes)
        assert all(i.is_directed for i in links) or all(
            not i.is_directed for i in links
        )
        self.is_directed = next(i.is_directed for i in links)
        self.links = set(links)
