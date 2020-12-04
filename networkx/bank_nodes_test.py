from pathlib import Path

import numpy as np
import pandas as pd
import plotly.offline as py
import plotly.graph_objects as go
import networkx as nx
import re

PATH_SRC = Path(__file__).resolve().parent
PATH_PROJECT = PATH_SRC.parent
PATH_DATA = PATH_PROJECT / 'data'
PATH_BANK = PATH_PROJECT / 'd3-network-analysis' / 'static' / 'data'

df_edge = pd.read_csv(str(PATH_BANK/'banking_links.csv'))
df_node = pd.read_csv(str(PATH_BANK/'banking_nodes.csv'))
print(df_edge.head())
print(df_node.head())

# build network graph
G = nx.Graph()

# add nodes
# https://networkx.org/documentation/stable/reference/classes/generated/networkx.Graph.add_node.html
for index, row in df_node.iterrows():
    # print(row['name'], row['type'], row['importance'], row['sentiment_emb'])
    G.add_node(row['name'], size=row['importance'])
# print(G.nodes)

# add edges
# https://networkx.org/documentation/stable/reference/classes/generated/networkx.Graph.add_edge.html
for index, row in df_edge.iterrows():
    # print(row['name'], row['type'], row['importance'], row['sentiment_emb'])
    G.add_edge(row['source'], row['target'], weight=row['weight'])
# print(G.edges)

# Get positions for the nodes in G
pos_ = nx.spring_layout(G)
# print(pos_)

# Find connected components
connected = list(nx.connected_components(G))
print('connected\n', connected)

# Find bridges
print("bridges:\n", list(nx.bridges(G)))

# Find Communities: https://networkx.org/documentation/stable/reference/algorithms/community.html
from networkx.algorithms import community
communities_generator = community.girvan_newman(G)
top_level_communities = next(communities_generator)
next_level_communities = next(communities_generator)
print("top_level_communities\n", top_level_communities)
print("next_level_communities\n", sorted(map(sorted, next_level_communities)))


# print(G.edges()[('OCBC', 'UOB')])

def make_edge(x, y, text, width):
    
    '''Creates a scatter trace for the edge between x's and y's with given width

    Parameters
    ----------
    x    : a tuple of the endpoints' x-coordinates in the form, tuple([x0, x1, None])
    
    y    : a tuple of the endpoints' y-coordinates in the form, tuple([y0, y1, None])
    
    width: the width of the line

    Returns
    -------
    An edge trace that goes between x0 and x1 with specified width.
    '''
    return  go.Scatter(x         = x,
                       y         = y,
                       line      = dict(width = width,
                                   color = 'cornflowerblue'),
                       hoverinfo = 'text',
                       text      = ([text]),
                       mode      = 'lines')

# For each edge, make an edge_trace, append to list
edge_trace = []
for edge in G.edges():
    
    if G.edges()[edge]['weight'] > 0:
        char_1 = edge[0]
        char_2 = edge[1]

        x0, y0 = pos_[char_1]
        x1, y1 = pos_[char_2]

        text   = char_1 + '--' + char_2 + ': ' + str(G.edges()[edge]['weight'])
        
        trace  = make_edge([x0, x1, None], [y0, y1, None], text,
                           0.3*G.edges()[edge]['weight']**1.25)

        edge_trace.append(trace)

# Make a node trace
node_trace = go.Scatter(x         = [],
                        y         = [],
                        text      = [],
                        textposition = "top center",
                        textfont_size = 10,
                        mode      = 'markers+text',
                        hoverinfo = 'none',
                        marker    = dict(color = [],
                                         size  = [],
                                         line  = None))
# For each node in G, get the position and size and add to the node_trace
for node in G.nodes():
    x, y = pos_[node]
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])
    node_trace['marker']['color'] += tuple(['cornflowerblue'])
    node_trace['marker']['size'] += tuple([30*G.nodes()[node]['size']])
    node_trace['text'] += tuple(['<b>' + node + '</b>'])

layout = go.Layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)


fig = go.Figure(layout = layout)

for trace in edge_trace:
    fig.add_trace(trace)

fig.add_trace(node_trace)

fig.update_layout(showlegend = False)

fig.update_xaxes(showticklabels = False)

fig.update_yaxes(showticklabels = False)

fig.show()
# py.plot(fig, filename='G_network.html')
