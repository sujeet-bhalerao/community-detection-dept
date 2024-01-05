import pandas as pd
from communities.algorithms import louvain_method
from communities.visualization import draw_communities
import numpy as np


data_comref = pd.read_csv('data/co_reference_matrix.csv', index_col=0)
# data_comjournals = pd.read_csv('data/shared_journals_matrix.csv', index_col=0)
# data_compubs = pd.read_csv('data/coauthored_papers_matrix.csv', index_col=0)
# data_comcite = pd.read_csv('data/common_citations_matrix.csv', index_col=0)


adj_matrix_ref = data_comref.values
# adj_matrix_journals = data_comjournals.values
# adj_matrix_compubs = data_compubs.values
# adj_matrix_comcite = data_comcite.values



communities_ref, frames_r = louvain_method(adj_matrix_ref)
# communities_journals, frames_j = louvain_method(adj_matrix_journals)
# communities_compubs, frames_c = louvain_method(adj_matrix_compubs)
# communities_comcite, frames_cc = louvain_method(adj_matrix_comcite)




faculty_names = data_comref.index.tolist()

def map_indices_to_names(community):
    return {faculty_names[index] for index in community}

communities_named_ref = [map_indices_to_names(community) for community in communities_ref]
# communities_named_journals = [map_indices_to_names(community) for community in communities_journals]
# communities_named_compubs = [map_indices_to_names(community) for community in communities_compubs]
# communities_named_comcite = [map_indices_to_names(community) for community in communities_comcite]




print("\nCommunities based on common references:\n", communities_named_ref)
# print("\nCommunities based on shared journals:\n", communities_named_journals)
# print("\nCommunities based on coauthored papers:\n", communities_named_compubs)
# print("\nCommunities based on common citations:\n", communities_named_comcite)



