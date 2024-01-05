import os
import glob
import json
import pandas as pd
import re
from collections import defaultdict

def read_json_file(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data

def get_references(data):
    return [reference for paper in data['Papers'].values() for reference in paper['References']]

def format_author_name(file_name):
    name_with_underscores = os.path.basename(file_name).replace('_papers.json', '')
    formatted_name = re.sub(r"(?<=\w)([A-Z])", r" \1", name_with_underscores)
    return formatted_name

path = os.getcwd()
paper_files = glob.glob(path + '/data/papers/*_papers.json')

refs_dict = defaultdict(set) # stores references for each author
matrix_dict = defaultdict(int) # stores co-reference counts

# iterate over all json files to collect references for each author
for file in paper_files:
    data = read_json_file(file)
    author_name = format_author_name(file) # get formatted name from filename
    references = get_references(data)
    refs_dict[author_name] = set(references)



# generate the co-reference counts
for author1, refs1 in refs_dict.items():
    for author2, refs2 in refs_dict.items():
        common_refs = refs1.intersection(refs2)
        matrix_dict[(author1, author2)] = len(common_refs)

# create matrix with co-reference counts
rows = list(refs_dict.keys())
matrix = pd.DataFrame(0, index=rows, columns=rows)

for authors, count in matrix_dict.items():
    author1, author2 = authors
    matrix.at[author1, author2] = count


matrix.to_csv(path + '/data/co_reference_matrix.csv')
