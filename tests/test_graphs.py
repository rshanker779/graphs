from itertools import combinations

from pytest_cases import parametrize_plus, fixture_ref

from graphs import Link, PathLink
from tests.conftest import (
    line_graph,
    complete_graph,
    disconnected_graph,
    directed_graph,
    cyclic_directed_graph,
)


@parametrize_plus(
    "graph",
    [
        fixture_ref(line_graph),
        fixture_ref(complete_graph),
        fixture_ref(disconnected_graph),
        fixture_ref(directed_graph),
        fixture_ref(cyclic_directed_graph),
    ],
)
def test_is_in_nodes(nodes, graph):
    assert all(graph.is_in_graph(node) for node in nodes)


@parametrize_plus(
    "graph,expected_order,expected_size",
    [
        (fixture_ref(line_graph), 5, 4),
        (fixture_ref(complete_graph), 5, 10),
        (fixture_ref(disconnected_graph), 5, 2),
        (fixture_ref(directed_graph), 5, 4),
        (fixture_ref(cyclic_directed_graph), 5, 3),
    ],
)
def test_graph_order_and_size(graph, expected_order, expected_size):
    assert graph.order == expected_order
    assert graph.size == expected_size


@parametrize_plus(
    "graph,node_1_index,node_2_index,are_neighbours",
    [
        (fixture_ref(line_graph), 0, 1, True),
        (fixture_ref(line_graph), 2, 3, True),
        (fixture_ref(line_graph), 0, 4, False),
        (fixture_ref(line_graph), 1, 3, False),
        (fixture_ref(disconnected_graph), 0, 1, True),
        (fixture_ref(disconnected_graph), 2, 3, True),
        (fixture_ref(disconnected_graph), 0, 3, False),
        (fixture_ref(disconnected_graph), 1, 2, False),
        (fixture_ref(directed_graph), 0, 1, True),
        (fixture_ref(directed_graph), 1, 0, False),
        (fixture_ref(directed_graph), 3, 4, True),
        (fixture_ref(directed_graph), 3, 0, False),
        (fixture_ref(cyclic_directed_graph), 0, 1, True),
        (fixture_ref(cyclic_directed_graph), 1, 0, False),
        (fixture_ref(cyclic_directed_graph), 1, 2, True),
        (fixture_ref(cyclic_directed_graph), 2, 0, True),
        (fixture_ref(cyclic_directed_graph), 2, 3, False),
    ]
    + [(fixture_ref(complete_graph), i, j, True) for i, j in combinations(range(5), 2)],
)
def test_graph_neighbours(nodes, graph, node_1_index, node_2_index, are_neighbours):
    assert (
        graph.are_neighbours(nodes[node_1_index], nodes[node_2_index]) == are_neighbours
    )


@parametrize_plus(
    "graph,node_index,expected_neighbouring_nodes",
    [
        (fixture_ref(line_graph), 0, {1}),
        (fixture_ref(line_graph), 1, {0, 2}),
        (fixture_ref(disconnected_graph), 0, {1}),
        (fixture_ref(disconnected_graph), 1, {0}),
        (fixture_ref(directed_graph), 0, {1, 3}),
        (fixture_ref(directed_graph), 1, {2}),
        (fixture_ref(cyclic_directed_graph), 0, {1}),
        (fixture_ref(cyclic_directed_graph), 1, {2}),
        (fixture_ref(cyclic_directed_graph), 2, {0}),
    ]
    + [(fixture_ref(complete_graph), i, set(range(5)) - {i}) for i in range(5)],
)
def test_neighbourhood(nodes, graph, node_index, expected_neighbouring_nodes):
    assert graph.get_neighbourhood(nodes[node_index]) == {
        nodes[i] for i in expected_neighbouring_nodes
    }


@parametrize_plus(
    "graph,node_index,expected_degree",
    [
        (fixture_ref(line_graph), 1, 2),
        (fixture_ref(disconnected_graph), 1, 1),
        (fixture_ref(directed_graph), 0, 2),
        (fixture_ref(cyclic_directed_graph), 1, 1),
    ]
    + [(fixture_ref(complete_graph), i, 4) for i in range(5)],
)
def test_node_degree_properties(nodes, graph, node_index, expected_degree):
    assert graph.get_degree(nodes[node_index]) == expected_degree


@parametrize_plus(
    "graph,degree_sequence,minimum_degree,maximum_degree",
    [
        (fixture_ref(line_graph), [1, 1, 2, 2, 2], 1, 2),
        (fixture_ref(complete_graph), [4] * 5, 4, 4),
        (fixture_ref(disconnected_graph), [0, 1, 1, 1, 1], 0, 1),
        (fixture_ref(directed_graph), [0, 0, 1, 1, 2], 0, 2),
        (fixture_ref(cyclic_directed_graph), [0, 0, 1, 1, 1], 0, 1),
    ],
)
def test_degree_properties(graph, degree_sequence, minimum_degree, maximum_degree):
    assert sorted(graph.degree_sequence) == degree_sequence
    assert graph.minimum_degree == minimum_degree
    assert graph.maximum_degree == maximum_degree


@parametrize_plus(
    "graph,k,expected_is_k_regular",
    [
        (fixture_ref(line_graph), 1, False),
        (fixture_ref(complete_graph), 1, False),
        (fixture_ref(complete_graph), 4, True),
        (fixture_ref(disconnected_graph), 2, False),
        (fixture_ref(directed_graph), 2, False),
        (fixture_ref(cyclic_directed_graph), 3, False),
    ],
)
def test_is_k_regular(graph, k, expected_is_k_regular):
    assert graph.is_k_regular(k) == expected_is_k_regular


@parametrize_plus(
    "graph,node_1_index,node_2_index,expected_is_possible,expected_number_paths,expected_distance",
    [
        (fixture_ref(line_graph), i, j, True, None, None)
        for i, j in combinations(range(5), 2)
    ]
    + [
        (fixture_ref(complete_graph), i, j, True, 16, 1)
        for i, j in combinations(range(5), 2)
    ]
    + [
        (fixture_ref(line_graph), 0, 4, True, 1, 4),
        (fixture_ref(line_graph), 1, 3, True, 1, 2),
        (fixture_ref(line_graph), 4, 3, True, 1, 1),
        (fixture_ref(disconnected_graph), 0, 1, True, 1, 1),
        (fixture_ref(disconnected_graph), 2, 3, True, 1, 1),
        (fixture_ref(disconnected_graph), 0, 2, False, 0, -1),
        (fixture_ref(disconnected_graph), 0, 3, False, 0, -1),
        (fixture_ref(disconnected_graph), 1, 2, False, 0, -1),
        (fixture_ref(disconnected_graph), 1, 3, False, 0, -1),
        (fixture_ref(directed_graph), 0, 1, True, 1, 1),
        (fixture_ref(directed_graph), 1, 0, False, 0, -1),
        (fixture_ref(directed_graph), 3, 4, True, 1, 1),
        (fixture_ref(directed_graph), 4, 3, False, 0, -1),
        (fixture_ref(cyclic_directed_graph), 0, 1, True, 1, 1),
        (fixture_ref(cyclic_directed_graph), 1, 2, True, 1, 1),
        (fixture_ref(cyclic_directed_graph), 2, 0, True, 1, 1),
        (fixture_ref(cyclic_directed_graph), 1, 0, True, 1, 2),
        (fixture_ref(cyclic_directed_graph), 0, 2, True, 1, 2),
        (fixture_ref(cyclic_directed_graph), 2, 1, True, 1, 2),
    ],
)
def test_is_path_possible(
    nodes,
    graph,
    node_1_index,
    node_2_index,
    expected_is_possible,
    expected_number_paths,
    expected_distance,
):
    path = graph.get_paths(nodes[node_1_index], nodes[node_2_index])
    assert path.is_possible == expected_is_possible
    if expected_number_paths is not None:
        assert len(path.paths) == expected_number_paths
    if expected_distance is not None:
        assert path.distance == expected_distance


@parametrize_plus(
    "graph,expected_connected,expected_cyclic,expected_eulerian,expected_dag",
    [
        (fixture_ref(line_graph), True, False, False, False),
        (fixture_ref(complete_graph), True, True, True, False),
        (fixture_ref(disconnected_graph), False, False, False, False),
        (fixture_ref(directed_graph), True, False, False, True),
        (fixture_ref(cyclic_directed_graph), False, True, False, False),
    ],
)
def test_global_properties(
    graph, expected_connected, expected_cyclic, expected_eulerian, expected_dag
):
    assert graph.is_connected == expected_connected
    assert graph.is_cyclic == expected_cyclic
    assert graph.is_eulerian == expected_eulerian
    assert graph.is_dag == expected_dag


@parametrize_plus(
    "graph,expected_chains",
    [
        (fixture_ref(line_graph), []),
        (fixture_ref(complete_graph), []),
        (fixture_ref(disconnected_graph), []),
        (fixture_ref(directed_graph), [[4, 3, 0], [2, 1, 0]]),
        (fixture_ref(cyclic_directed_graph), []),
    ],
)
def test_dag_dependency_chain(nodes, graph, expected_chains):
    chain = graph.dependency_chain
    if chain:
        for expected_chain in expected_chains:
            expected_nodes = list(map(lambda x: nodes[x], expected_chain))
            sub_list = [i for i in chain if i in expected_nodes]
            assert sub_list == expected_nodes
    else:
        assert chain == expected_chains


def test_line_graph(nodes, line_links, line_graph):

    for node in nodes:
        assert line_graph.get_connected_component(node) == set(nodes)
        assert line_graph.is_in_graph(node)
    assert set(nodes) in line_graph.connected_components


def test_complete_graph(complete_graph, nodes):

    for node in nodes:
        assert complete_graph.get_connected_component(node) == set(nodes)
    assert set(nodes) in complete_graph.connected_components


def test_disconnected_graph(disconnected_graph, nodes):

    n1, n2, n3, n4, n5 = nodes

    path = disconnected_graph.get_paths(n1, n2)
    assert path.paths == [(PathLink(n1, n2, Link(n1, n2)),)]
    assert disconnected_graph.get_connected_component(n1) == {n1, n2}
    assert disconnected_graph.get_connected_component(n3) == {n3, n4}
    assert {n1, n2} in disconnected_graph.connected_components
    assert {n3, n4} in disconnected_graph.connected_components
    assert {n5} in disconnected_graph.connected_components


def test_directed_graph(directed_graph, nodes):

    n1, n2, n3, n4, n5 = nodes

    path = directed_graph.get_paths(n1, n2)
    assert path.paths == [(PathLink(n1, n2, Link(n1, n2, True)),)]
    assert path.distance == 1
    path = directed_graph.get_paths(n2, n1)
    assert path.paths == []
    assert directed_graph.get_connected_component(n1) == set(nodes)
