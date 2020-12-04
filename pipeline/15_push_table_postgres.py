import sys
from pathlib import Path

import pickle
import pandas as pd

PATH_DB = Path.home()/Path('db/')
sys.path.append(str(PATH_DB))
from db import DB

def get_db(db):
    return DB(db)
# initialize DB
db_web = get_db('network_analysis')


# load data
df_edges = pd.read_csv('14_edge_df_final.csv')
df_news_edge = pd.read_csv('14_news_edge_df.csv')
df_nodes = pd.read_csv('14_node_df.csv')
df_nodes_edge = pd.read_csv('14_news_node_df.csv') 

print("df_edges\n", df_edges.head())
print("df_news_edge\n", df_news_edge.head())
print("df_nodes\n", df_nodes.head())
print("df_nodes_edge\n", df_nodes_edge.head())

# save data to DB
df_edges.to_sql('edge', con=db_web.sql_engine, if_exists='replace', index=False)
df_news_edge.to_sql('news_edges', con=db_web.sql_engine, if_exists='replace', index=False)
df_nodes.to_sql('node', con=db_web.sql_engine, if_exists='replace', index=False)
df_nodes_edge.to_sql('news_node', con=db_web.sql_engine, if_exists='replace', index=False)
