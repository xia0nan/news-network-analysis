import pickle
import pandas as pd
import numpy as np

# read pickle from step 03
with open('13_out.pkl', 'rb') as f:
    api_out = pickle.load(f)

# print(api_out)

### get node and news_node
temp_df = api_out.copy()

# import uuid
# temp_df['node_id'] = [uuid.uuid4() for _ in range(len(temp_df.index))]
temp_df['node_id'] = temp_df['permid']

# print(temp_df)

# news_node table
news_node_df = temp_df[['news_id', 'node_id']].copy()
news_node_df.drop_duplicates(inplace=True, ignore_index=True)
print(news_node_df)
news_node_df.to_csv("14_news_node_df.csv", index=False)

# node table
node_df = temp_df[['node_id', 'name', 'dtype', 'permid']].copy()
node_df.drop_duplicates(inplace=True, ignore_index=True)
print(node_df)
node_df.to_csv("14_node_df.csv", index=False)

### edge table
temp_df = api_out.copy()
temp_df2 = api_out.copy()

# join by news_id
temp_14 = pd.merge(temp_df, temp_df2, on='news_id')

# remove join by itself
temp_14 = temp_14[temp_14['name_x']!=temp_14['name_y']]

def get_edge_id(row):
    # assume permid is length 10 digits
    if (row['permid_x']) < (row['permid_y']):
        # assume permid_x and permid_y are string
        edge_id = row['permid_x'] + row['permid_y']
    elif (row['permid_x']) > (row['permid_y']):
        edge_id = row['permid_y'] + row['permid_x']
    else:
        print(row)
        # raise "same permid"
        edge_id = row['permid_x'] + row['permid_y']
    return edge_id

# assign edge id
temp_14['edge_id'] = temp_14.apply (lambda row: get_edge_id(row), axis=1)

temp_14.to_csv("14_edge_df_raw.csv", index=False)

# news_edge table
news_edge = temp_14[['news_id', 'edge_id']].copy()
print("news_edge", news_edge)
news_edge.drop_duplicates(inplace=True, ignore_index=True)
# print(news_node_df)
news_edge.to_csv("14_news_edge_df.csv", index=False)

# final edge_df
edge = temp_14[['edge_id', 'permid_x', 'permid_y']]
edge['source_node_id'] = pd.np.minimum(edge['permid_x'], edge['permid_y'])
edge['target_node_id'] = pd.np.maximum(edge['permid_x'], edge['permid_y'])
# print('edge\n', edge)
edge = edge[['edge_id', 'source_node_id', 'target_node_id']]
# print('edge\n', edge)

# remove duplicates
edge = edge.drop_duplicates()
print('edge\n', edge)

edge.to_csv("14_edge_df_final.csv", index=False)
