import json
import os
import numpy as np
import pandas as pd
from collections import Counter


directory = './data/citations/'
prof_cited_papers = {}


for filename in os.listdir(directory):
    if filename.endswith('.json'):  
        with open(os.path.join(directory, filename), 'r') as f:
            data = json.load(f)
        name = filename.split('_')[0]
        prof_cited_papers[name] = []
        for papers in data.values():
            if papers:
                for paper in papers:
                    prof_cited_papers[name].append(paper[1])  



professors = list(prof_cited_papers.keys())
n = len(professors)
similarity_matrix = np.zeros((n, n))

for i in range(n):
    for j in range(n):
        counter_i = Counter(prof_cited_papers[professors[i]])
        counter_j = Counter(prof_cited_papers[professors[j]])
        common_citations = (counter_i & counter_j).values()  
        similarity_matrix[i][j] = sum(common_citations)


df = pd.DataFrame(similarity_matrix, index=professors, columns=professors)
df.to_csv('common_citations_matrix.csv')


# for professor in prof_cited_papers:
#     print(f'The total number of citations for professor {professor} is: {len(prof_cited_papers[professor])}')
