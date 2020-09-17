import os
import sys
from pathlib import Path
import random

import numpy as np
import pandas as pd

PATH_SRC = Path(__file__).resolve().parent
PATH_PROJECT = PATH_SRC.parent
PATH_DATA = PATH_PROJECT / 'data'

target_link_name = 'banking_links.csv'
target_node_name = 'banking_nodes.csv'

target_path = "../d3-network-analysis/static/data/"

# read original data
df = pd.read_csv(str(PATH_DATA/'network_banks_temp4.csv'))
df.dropna(inplace=True)

### banking_links ###

# rename columns
df = df.rename(columns={'source_company': 'source', 'target_company': 'target', 'c_news': 'weight'})
# add link_type, all ORGANIZATION
df['link_type'] = 'ORGANIZATION'
# reduce weights
df['weight'] //= 2

# print(df.head())

# df.to_csv(target_path + target_link_name, index=False)

### banking_nodes ###
df2 = df.copy()

node_dict = {}

df_temp = df[['source','weight']].copy()
df_temp = df_temp.groupby(['source']).sum().reset_index()

# print(df_temp)

node_list = df_temp['source'].tolist()
node_size = df_temp['weight'].tolist()

node_dict = dict(zip(node_list, node_size))

df_temp = df[['target','weight']].copy()
df_temp = df_temp.groupby(['target']).sum().reset_index()

# print(df_temp)

node_list = df_temp['target'].tolist()
node_size = df_temp['weight'].tolist()

temp_node_dict = dict(zip(node_list, node_size))

for key in temp_node_dict:
    if key not in node_dict:
        node_dict[key] = temp_node_dict[key]

# get max weights

max_weight = node_dict[max(node_dict, key=node_dict.get)]
# print("max_weight", max_weight)

# print(node_dict)

df_node = pd.DataFrame(node_dict.items(), columns=['name', 'importance'])
df_node['importance'] /= max_weight
# print(df_node)

# assign type
df_node['type'] = 'ORGANIZATION'

# assign sentiment
sentiment_list = [-100, -50, 0, 50, 100]
df_node['sentiment_emb'] = np.random.choice(sentiment_list, size=len(df_node))
print(df_node)

df_node.to_csv(target_path + target_node_name, index=False)

