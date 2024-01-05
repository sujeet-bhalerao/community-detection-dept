import json
import os
import glob
import pandas as pd
import re
from collections import defaultdict

def read_json_file(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data

def get_journals(data):
    return [paper['Journal_Name'][0] for paper in data['Papers'].values() if paper['Journal_Name']]

def format_author_name(file_name):
    name_with_underscores = os.path.basename(file_name).replace('_papers.json', '')
    formatted_name = re.sub(r"(?<=\w)([A-Z])", r" \1", name_with_underscores)
    return formatted_name

path = os.getcwd()
paper_files = glob.glob(path + '/data/papers/*_papers.json')

journals_dict = defaultdict(set) # stores journals for each author
matrix_dict = defaultdict(int) # stores shared journal counts

# iterate over all json files to get each author's journals and name
for file in paper_files:
    data = read_json_file(file)
    author_name = format_author_name(file) 
    journals = get_journals(data)
    journals_dict[author_name] = set(journals)

# generate the shared journal counts
for author1, journs1 in journals_dict.items():
    for author2, journs2 in journals_dict.items():
        common_journs = journs1.intersection(journs2)
        matrix_dict[(author1, author2)] = len(common_journs)

# create a matrix with shared journal counts
rows = list(journals_dict.keys())
matrix = pd.DataFrame(0, index=rows, columns=rows)

for authors, count in matrix_dict.items():
    author1, author2 = authors
    matrix.at[author1, author2] = count

matrix.to_csv(path + '/data/shared_journals_matrix.csv')
