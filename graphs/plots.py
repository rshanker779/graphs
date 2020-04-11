import numpy as np
from matplotlib import pyplot as plt

from graphs.graph_properties import BaseGraphProperties


class GraphPlotter(BaseGraphProperties):
    def plot_graph(self) -> plt.Figure:
        n = len(self.nodes)
        point_map = {i: j for i, j in enumerate(self.nodes)}
        node_map = {j.id: self._get_roots_of_unity(i, n) for i, j in point_map.items()}
        complex_repns = [self._get_roots_of_unity(k, n) for k in point_map]
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
        return plt.gcf()

    @staticmethod
    def _get_roots_of_unity(k, n) -> complex:
        return np.exp(2 * np.pi * 1j * k / n)
