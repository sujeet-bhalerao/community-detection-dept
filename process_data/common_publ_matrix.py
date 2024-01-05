import os
import glob
import json
import pandas as pd
from collections import defaultdict
import re 

def read_json_file(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data

def format_author_name(file_name):
    name_with_underscores = os.path.basename(file_name).replace('_papers.json', '')
    formatted_name = re.sub(r"(?<=\w)([A-Z])", r" \1", name_with_underscores)
    return formatted_name


author_papers = defaultdict(list)
path = os.getcwd()
paper_files = glob.glob(path + '/data/papers/*_papers.json')

# iterate over all json files to get each author's papers
# for file in paper_files:
#     data = read_json_file(file)
#     author_name = format_author_name(file)
#     author_papers[author_name] = [paper['PaperID'] for paper in data['Papers'].values()]

for file in paper_files:
    data = read_json_file(file)
    if data is None:
        print(f"Data is None for file: {file}")
        continue
    if 'Papers' not in data:
        print(f"'Papers' key not found in file: {file}")
        continue
    author_name = format_author_name(file)
    author_papers[author_name] = [paper['PaperID'] for paper in data['Papers'].values()]


coauthored_papers_matrix = defaultdict(int)  # stores coauthored paper counts

for author1, papers1 in author_papers.items():
    for author2, papers2 in author_papers.items():
        shared_papers = set(papers1) & set(papers2)  # intersection of two paper lists
        coauthored_papers_matrix[(author1, author2)] = len(shared_papers)

rows = list(author_papers.keys())
matrix_df = pd.DataFrame(0, columns=rows, index=rows)

for authors, count in coauthored_papers_matrix.items():
    matrix_df.at[authors[0], authors[1]] = count

matrix_df.to_csv(path + '/data/coauthored_papers_matrix.csv')
