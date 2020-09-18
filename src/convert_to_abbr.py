import os
import sys
from pathlib import Path
import random

import numpy as np
import pandas as pd

PATH_SRC = Path(__file__).resolve().parent
PATH_PROJECT = PATH_SRC.parent
PATH_DATA = PATH_PROJECT / 'data'

original_link_name = 'banking_links copy 2.csv'
original_node_name = 'banking_nodes copy 2.csv'

target_link_name = 'banking_links.csv'
target_node_name = 'banking_nodes.csv'
abbr_name = 'abbreviations.csv'

target_path = "../d3-network-analysis/static/data/"

# read original data
df_link = pd.read_csv(target_path + original_link_name)
# print(df_link.head())

df_abbr = pd.read_csv(target_path + abbr_name)
# print(df_abbr.head())

df_temp = df_link.join(df_abbr.set_index('name'), on='source')
# print(df_temp)

df_temp = df_temp.rename(columns={'source': 'to_drop', 'abbr': 'source'})
# print(df_temp)

df_temp = df_temp[['source', 'target', 'weight', 'link_type']]
# print(df_temp)

df_temp = df_temp.join(df_abbr.set_index('name'), on='target')
# print(df_temp)

df_temp = df_temp.rename(columns={'target': 'to_drop', 'abbr': 'target'})
# print(df_temp)

df_temp = df_temp[['source', 'target', 'weight', 'link_type']]
# print(df_temp)

df_temp.to_csv(target_path + target_link_name, index=False)

# read original data
df_node = pd.read_csv(target_path + original_node_name)
# print(df_node.head())

df_temp = df_node.join(df_abbr.set_index('name'), on='name')
# print(df_temp)

df_temp = df_temp.rename(columns={'name': 'to_drop', 'abbr': 'name'})
# print(df_temp)

df_temp = df_temp[['name', 'type', 'importance', 'sentiment_emb']]
# print(df_temp)

df_temp.to_csv(target_path + target_node_name, index=False)
