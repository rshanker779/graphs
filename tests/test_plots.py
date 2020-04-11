import matplotlib.pyplot as plt
from pytest_cases import parametrize_plus, fixture_ref

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
def test_graph_plot(graph,):
    res = graph.plot_graph()
    assert isinstance(res, plt.Figure)
