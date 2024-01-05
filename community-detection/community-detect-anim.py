import pandas as pd
from communities.algorithms import louvain_method
import numpy as np
from communities.algorithms import louvain_method
from communities.visualization import louvain_animation

co_ref_matrix = pd.read_csv('data/co_reference_matrix.csv', index_col=0)
n = co_ref_matrix.shape[0]

adj_matrix_ref = pd.DataFrame(np.zeros((n, n)), index=co_ref_matrix.index, columns=co_ref_matrix.columns)

percentage_threshold = 0.02

for i in range(n):
    for j in range(n):
        if i != j:  
            total_citations = co_ref_matrix.iloc[i, i] + co_ref_matrix.iloc[j, j]
            shared_citations = co_ref_matrix.iloc[i, j]
            if total_citations > 0 and (shared_citations / total_citations) >= percentage_threshold:
                adj_matrix_ref.iloc[i, j] = 1

adj_matrix_ref.to_csv('adjacency_matrix.csv')

adj_matrix_ref = adj_matrix_ref.values

communities_ref, frames_r = louvain_method(adj_matrix_ref)

print(adj_matrix_ref)

faculty_names = co_ref_matrix.index.tolist()

def map_indices_to_names(community):
    return {faculty_names[index] for index in community}

communities_named_ref = [map_indices_to_names(community) for community in communities_ref]

print("\nCommunities based on common references:\n", communities_named_ref)


import matplotlib.pyplot as plt
import networkx as nx

adj_matrix_ref = pd.read_csv('adjacency_matrix.csv', index_col=0)

G = nx.from_pandas_adjacency(adj_matrix_ref)

pos = nx.spring_layout(G, seed=42)  

last_names = {full_name: full_name.split()[0] for full_name in faculty_names}


node_labels = {node: last_names[node] for node in G.nodes()}

node_labels = {node: node for node in G.nodes()}

color_map = []
for node in G.nodes():
    for i, community in enumerate(communities_named_ref):
        if node in community:
            color_map.append(i) 
            break


plt.figure(figsize=(15, 15))
nx.draw_networkx_edges(G, pos, alpha=0.5)
nx.draw_networkx_nodes(G, pos, node_color=color_map, cmap=plt.cm.jet, node_size=100)
nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=6)

plt.title('Communities based on common references')
plt.axis('off')
plt.savefig("viz_graph.png")