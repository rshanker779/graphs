import re

import pytest

import graphs
from graphs.exceptions import InvalidDictionaryException


@pytest.fixture
def bad_graph_dict():
    return {1: {2, 3}, 2: {1}}


@pytest.fixture
def line_graph_dict():
    return {0: {1}, 1: {2}, 2: {3}, 3: {4}, 4: set()}


def test_incorrect_graph_dict(bad_graph_dict):
    with pytest.raises(InvalidDictionaryException) as exc:
        graphs.Graph.from_graph_dictionary(bad_graph_dict, True)
    assert "3" in str(exc.value)
    assert re.match(".*Found node.*not present.*keys.*", str(exc.value)) is not None


def test_matching_graphs(line_graph, line_graph_dict):
    graph = graphs.Graph.from_graph_dictionary(line_graph_dict, False)
    assert graph.nodes == line_graph.nodes
    assert graph.links == line_graph.links
