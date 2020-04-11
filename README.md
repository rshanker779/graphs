# Graphs

Graph theory in Python

Construct a graph object by building up links and nodes
```python
import graphs
n1, n2, n3 = [graphs.Node()]*3
links = [graphs.Link(n1, n2),graphs.Link(n2, n3)]
graph = graphs.Graph([n1, n2, n3], links)
```

Or specifying via a dictionary
```python
graph_dict = {1:{2}, 2:{3}, 3:set()}
graph = graphs.Graph.from_graph_dictionary(graph_dict, is_directed=False)
```

Can then query and interact with the resulting object
```python
graph.order
graph.size
graph.are_neighbours(n1, n2)
graph.plot_graph()
graph.get_degree(n1)
graph.degree_sequence
graph.get_paths(n1, n2)
graph.connected_components
graph.is_cyclic
graph.is_dag
graph.is_eulerian
```

Can build a dependency chain for a DAG by
```python
graph.dependency_chain
```