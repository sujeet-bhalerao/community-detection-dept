import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

adj_matrix_ref = pd.read_csv('adjacency_matrix.csv', index_col=0)

G = nx.from_pandas_adjacency(adj_matrix_ref)

plt.figure(figsize=(15, 15))
pos = nx.circular_layout(G)  # positions for all nodes
nx.draw_networkx_nodes(G, pos, node_size=300)
nx.draw_networkx_edges(G, pos, width=2.0, alpha=0.7)
nx.draw_networkx_labels(G, pos, font_size=8)

plt.axis('off')
plt.savefig("viz_graph_circular.png")
