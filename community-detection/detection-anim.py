import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
import networkx as nx

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

last_names = {full_name: full_name.split()[-1] for full_name in faculty_names}

color_map = []
for node in G.nodes():
    for i, community in enumerate(communities_named_ref):
        if node in community:
            color_map.append(i) 
            break

        
edge_trace = go.Scatter(
    x=[],
    y=[],
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_trace['x'] += tuple([x0, x1, None])
    edge_trace['y'] += tuple([y0, y1, None])

node_trace = go.Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers+text',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='Jet',
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Community',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=2)))

for node in G.nodes():
    x, y = pos[node]
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])
    node_trace['text'] += tuple([last_names[node]])


for node, adjacencies in enumerate(G.adjacency()):
    node_trace['marker']['color'] += tuple([color_map[node]])


fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='<br>Communities with common reference data',
                    titlefont=dict(size=16),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    annotations=[dict(
                        text="",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002)],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

plot(fig, filename='Professor_Co-References.html')
