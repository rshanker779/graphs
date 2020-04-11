from typing import List, Optional, Hashable

import rshanker779_common as utils


class Node(utils.StringMixin, utils.EqualsMixin):
    _id = 0

    def __init__(self, identifier: Optional[Hashable] = None):
        if identifier is None:
            identifier = self.__class__._id
            self.__class__._id += 1
        self.id = identifier


class Link(utils.StringMixin, utils.EqualsMixin):
    def __init__(self, node_1: Node, node_2: Node, is_directed: bool = False):
        super().__init__()
        self.node_1 = node_1
        self.node_2 = node_2
        self.is_directed = is_directed

    @property
    def nodes(self) -> List[Node]:
        return [self.node_1, self.node_2]
